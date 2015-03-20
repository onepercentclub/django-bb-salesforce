import logging
import re
import urllib2

from surlex import Surlex

from decimal import Decimal

from os import path

from pytz.exceptions import AmbiguousTimeError

from datetime import datetime
from django.utils import timezone

from django.core.files import File

from django.template.defaultfilters import slugify

class Mapping(object):
    """ Base class for mappings. """

    def __call__(self, instance, from_field):
        """ Just wrap to a more verbose map function. """

        return self.map(instance, from_field)

    def __repr__(self):
        return u'<%s>' % self.__class__.__name__


class NullMapping(Mapping):
    """ Mapping that, essentially just throws away the data. """

    def map(self, instance, to_field):
        return ''


class StaticMapping(Mapping):
    """
    Mapping that returns a given value
    """

    def __init__(self, value):
        self.value = value

    def map(self, instance, to_field):
        return {to_field: self.value}


class IdentityMapping(Mapping):
    """
    """

    def __init__(self, from_field=None):
        self.from_field = from_field

    def get_to_field(self, from_field):
        if self.to_field:
            return self.to_field
        return from_field

    def map_value(self, old_value):
        """
        Convenient wrapping function for filtering values.
        """
        return old_value

    def map(self, from_instance, to_field):
        old_value = getattr(from_instance, self.from_field)
        new_value = self.map_value(old_value)
        return {to_field: new_value}


class StringMapping(IdentityMapping):
    """
    Identity mapping but for strings returns a default value when it is none.
    """

    def __init__(self, from_field=None, default=''):
        self.default = default
        super(StringMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_value = super(StringMapping, self).map_value(old_value)
        if not old_value:
            return self.default
        return old_value


class UserOrAnonymousMapping(IdentityMapping):
    """
    Returns full name for user or "Anonymous" if no user None.
    """

    def __init__(self, from_field=None, default='Anonymous'):
        self.default = default
        super(UserOrAnonymousMapping, self).__init__(from_field)

    def map_value(self, old_value):
        user = super(UserOrAnonymousMapping, self).map_value(old_value)
        if not user:
            return self.default
        return user.get_full_name()


class MethodMapping(IdentityMapping):
    """
    Runs a method on the from_instance with given params (if any)
    """

    def __init__(self, from_field=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super(MethodMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_method = super(MethodMapping, self).map_value(old_value)
        new_value = old_method(*self.args, **self.kwargs)
        return new_value


class ImageMapping(StringMapping):
    """
    Return a image path.
    """
    def map_value(self, old_value):
        old_value = super(ImageMapping, self).map_value(old_value)
        if not old_value:
            return self.default
        return str(old_value)


class DateTimeMapping(IdentityMapping):
    """
    Return a Datetime with default None
    """

    def __init__(self, from_field=None, default=None):
        self.default = default
        super(DateTimeMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_value = super(DateTimeMapping, self).map_value(old_value)
        if not old_value:
            return self.default
        return old_value


class DateMapping(IdentityMapping):
    """
    Return a Date (from datetime) with default None
    """

    def __init__(self, from_field=None, default=None):
        self.default = default
        super(DateMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_value = super(DateMapping, self).map_value(old_value)
        if not old_value:
            return self.default
        return old_value.date()


class EuroMapping(IdentityMapping):
    """
    Return an amount with default 0
    """
    def __init__(self, from_field=None, default=0):
        self.default = default
        super(EuroMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_value = super(EuroMapping, self).map_value(old_value)
        if not old_value:
            return self.default
        return "%01.2f" % (old_value)


class EmailMapping(StringMapping):
    """
    Identity mapping but for email returns '' if email not valid.
    """
    def map_value(self, old_value):
        re_email = re.compile("^[A-Z0-9._%+-/!#$%&'*=?^_`{|}~]+@[A-Z0-9.-]+\\.[A-Z]{2,18}$")
        old_value = super(StringMapping, self).map_value(old_value)
        if old_value == None or not re_email.match(old_value.upper()):
            return ''
        return old_value


class CropMapping(StringMapping):
    """
    Subclass of the IdentityMapping, doing automated cropping of field data
    during the mapping.
    """
    def __init__(self, from_field, length, default=''):
        self.length = length
        super(CropMapping, self).__init__(from_field, default)

    def map_value(self, old_value):
        old_value = super(CropMapping, self).map_value(old_value)
        return old_value[:self.length]


class ConcatenateMapping(StringMapping):
    """
    Concatenate (string) fields into one value.
    """
    def __init__(self, from_fields, concatenate_str=' '):
        self.from_fields = from_fields
        self.concatenate_str = concatenate_str
        super(ConcatenateMapping, self).__init__()
        
    def map(self, from_instance, to_field):
        values = []
        for field in self.from_fields:
            values.append(getattr(from_instance, field))
        new_value = self.concatenate_str.join(values)
        return {to_field: new_value}


class TagsMapping(StringMapping):
    """
    Turn tags into a comma separated list
    """
    def map_value(self, old_value):
        old_value = super(StringMapping, self).map_value(old_value)
        tags = []
        for tag in old_value.all():
            tags.append(str(tag))
        return ", ".join(tags)[:255]


class RelatedMapping(StringMapping):
    """
    Gets the value of a related object or '' if it doesn't exist.
    """
    def map(self, from_instance, to_field):
        obj, field = self.from_field.split('.')
        if not hasattr(from_instance, obj):
            return {to_field: ''}
        related = getattr(from_instance, obj, None)
        if related:
            new_value = getattr(related, field, '')
            return {to_field: new_value}
        return {to_field: ''}


class StreetMapping(StringMapping):
    """
    Gets the street (line1 + line2)  of an address object or '' if it doesn't exist.
    """
    def map(self, from_instance, to_field):
        address = getattr(from_instance, self.from_field, None)
        if address:
            new_value = u'{0} {1}'.format(getattr(address, 'line1'), getattr(address, 'line2'))
            new_value = new_value.strip()
            return {to_field: new_value}
        return {to_field: ''}


class ChoiceMapping(StringMapping):
    """
    Turn tags into a comma seprated list
    """
    def __init__(self, from_field=None, choices_list=None):
        self.choices_list = choices_list
        super(StringMapping, self).__init__(from_field)

    def map(self, from_instance, to_field):
        from_field = self.from_field
        if self.choices_list:
            old_value = str(getattr(from_instance, from_field))
            return self.choices_list.values[old_value].title()
        display_value = "get_{0}_display".format(from_field)
        old_value = getattr(from_instance, display_value)()
        return {to_field: old_value}


class CountryMapping(IdentityMapping):
    """
    Map a country name or '' if no country set.
    """
    def map(self, from_instance, to_field):
        # Check if the country is in a related object (e.g. 'address.country')
        if "." in self.from_field:
            obj, field = self.from_field.split('.')
            related = getattr(from_instance, obj, None)
            if related:
                new_value = getattr(related, field, '')
                if new_value:
                    return {to_field: new_value.name.encode('utf-8')}
                return {to_field: ''}
            else:
                return {to_field: ''}
        else:
            new_value = getattr(from_instance, self.from_field)

            if new_value:
                return {to_field: new_value.name.encode('utf-8')}
        return {to_field: ''}


class SubRegionMapping(IdentityMapping):
    """
    Map a sub-region name name or '' if no country set.
    """
    def map(self, from_instance, to_field):
        # Check if the country is in a related object (e.g. 'address.country')
        if "." in self.from_field:
            obj, field = self.from_field.split('.')
            related = getattr(from_instance, obj, None)
            if related:
                country = getattr(related, field, '')
                if country:
                    return {to_field: country.subregion.name.encode('utf-8')}
                return {to_field: ''}
            else:
                return {to_field: ''}
        else:
            country = getattr(from_instance, self.from_field)

            if country:
                return {to_field: country.subregion.name.encode('utf-8')}
        return {to_field: ''}


class RegionMapping(IdentityMapping):
    """
    Map a region name name or '' if no country set.
    """
    def map(self, from_instance, to_field):
        # Check if the country is in a related object (e.g. 'address.country')
        if "." in self.from_field:
            obj, field = self.from_field.split('.')
            related = getattr(from_instance, obj, None)
            if related:
                country = getattr(related, field, '')
                if country:
                    return {to_field: country.subregion.region.name.encode('utf-8')}
                return {to_field: ''}
            else:
                return {to_field: ''}
        else:
            country = getattr(from_instance, self.from_field)

            if country:
                return {to_field: country.subregion.region.name.encode('utf-8')}
        return {to_field: ''}


class SalesforceObjectMapping(IdentityMapping):
    """
    Map to a Salesforce object.
    """

    def __init__(self, from_field=None, sf_model=None):
        self.sf_model = sf_model
        super(SalesforceObjectMapping, self).__init__(from_field)

    def map(self, from_instance, to_field):
        object_id = getattr(from_instance, '{0}_id'.format(self.from_field))

        objs = self.sf_model.objects.filter(external_id=object_id).all()
        if objs.count():
            sf_object = objs[0]
            return {to_field: sf_object}
        return {to_field: None}


class OrderPaymentMethodMapping(StringMapping):
    """
    Returns the payment method based on an order
    """

    def map_value(self, old_value):
        order = super(StringMapping, self).map_value(old_value)
        new_value = order.order_payment.method_name
        return new_value
