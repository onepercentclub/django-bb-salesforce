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

    def __repr__(self):
        return u'<%s>' % self.__class__.__name__

class IdentityMapping(Mapping):
    """
    """
    instance = None

    def __call__(self, instance=None):
        """ Just wrap to a more verbose set_instance function. """
        self.set_instance(instance)
        return self

    def __init__(self, from_field=None):
        self.from_field = from_field

    def get_field(self, instance=None, from_field=None):
        """
        Method to get nested attributes "order.user"
        """
        if not instance:
            instance = self.instance

        if not from_field:
            from_field = self.from_field

        attributes = from_field.split(".")
        obj = instance
        for i in attributes:
            try:
                obj = getattr(obj, i)
            except AttributeError:
                return None
        return obj

    def set_instance(self, instance):
        self.instance = instance

    def map_value(self, old_value):
        """
        Convenient wrapping function for filtering values.
        """
        return old_value

    def map(self):
        old_value = self.get_field()
        new_value = self.map_value(old_value)
        return new_value

    def to_field(self):
        return self.map()

    def to_csv(self):
        new_value = self.map()
        if isinstance(new_value, bool):
            if new_value:
                return '1'
            else:
                return '0'
        if isinstance(new_value, int):
            new_value = str(new_value)
        if isinstance(new_value, unicode):
            return new_value.encode('utf-8')
        else:
            return new_value


class StaticMapping(IdentityMapping):
    """
    Mapping that returns a given value
    """

    def map(self):
        # from_field will just be a string here.
        return self.from_field


class EmptyMapping(IdentityMapping):
    def map_value(self, old_value):
        return ''


class StringMapping(IdentityMapping):
    """
    Identity mapping but for strings returns a default value when it is none
    """

    def __init__(self, from_field=None, default=''):
        self.default = default
        super(StringMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_value = super(StringMapping, self).map_value(old_value)
        if not old_value:
            return self.default
        if not old_value.strip():
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
    Runs a method on the instance with given params (if any)
    """

    def __init__(self, from_field=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super(MethodMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_method = super(MethodMapping, self).map_value(old_value)
        new_value = old_method(*self.args, **self.kwargs)
        return new_value


class ImageMapping(IdentityMapping):
    """
    Return a image path.
    """
    def map_value(self, old_value):
        old_value = super(ImageMapping, self).map_value(old_value)
        if not old_value:
            return ''
        return str(old_value)


class DateTimeMapping(IdentityMapping):
    """
    Return a Datetime with default None
    """

    def __init__(self, from_field, date_format="%Y-%m-%dT%H:%M:%S.000Z", default=None):
        self.date_format = date_format
        self.default = default
        super(DateTimeMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_value = super(DateTimeMapping, self).map_value(old_value)
        if not old_value:
            return self.default
        return old_value

    def to_csv(self):
        new_value = super(DateTimeMapping, self).to_csv()
        if new_value:
            return new_value.strftime(self.date_format)
        return ''


class DateMapping(DateTimeMapping):
    """
    Return a Date (from datetime) with default None/''
    """

    def __init__(self, from_field=None, date_format="%Y-%m-%d", default=None):
        super(DateMapping, self).__init__(from_field, date_format, default)


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
            old_value = self.default
        return "%01.2f" % (old_value)

class EuroCentMapping(IdentityMapping):
    """
    Return an amount in euro with default 0
    """
    def __init__(self, from_field=None, default=0):
        self.default = default
        super(EuroCentMapping, self).__init__(from_field)

    def map_value(self, old_value):
        old_value = super(EuroCentMapping, self).map_value(old_value)
        if not old_value:
            old_value = self.default
        return "%01.2f" % (old_value / 100)

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

    def map(self):
        values = []
        for field in self.from_fields:
            values.append(getattr(self.instance, field))
        new_value = self.concatenate_str.join(values)
        return new_value


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
    Gets the value of a related object or the default value if it doesn't exist.
    """
    def map(self):
        obj, field = self.from_field.split('.')
        if not hasattr(self.instance, obj):
            return self.default
        related = getattr(self.instance, obj, None)
        if related:
            new_value = getattr(related, field, '')
            return new_value
        return self.default


class StreetMapping(StringMapping):
    """
    Gets the street (line1 + line2)  of an address object or '' if it doesn't exist.
    """
    def map(self):
        address = getattr(self.instance, self.from_field, None)
        if address:
            new_value = u'{0} {1}'.format(getattr(address, 'line1'), getattr(address, 'line2'))
            new_value = new_value.strip()
            return new_value
        return ''


class ChoiceMapping(StringMapping):
    """
    Turn tags into a comma seprated list
    """
    def __init__(self, from_field=None, choices_list=None):
        self.choices_list = choices_list
        super(StringMapping, self).__init__(from_field)

    def map(self):
        from_field = self.from_field
        if self.choices_list:
            old_value = str(getattr(self.instance, from_field))
            return self.choices_list.values[old_value].title()
        display_value = "get_{0}_display".format(from_field)
        old_value = getattr(self.instance, display_value)()
        return  old_value


class CountryMapping(IdentityMapping):
    """
    Map a country name or '' if no country set.
    """
    def map(self):
        # Check if the country is in a related object (e.g. 'address.country')
        if "." in self.from_field:
            obj, field = self.from_field.split('.')
            related = getattr(self.instance, obj, None)
            if related:
                new_value = getattr(related, field, '')
                if new_value:
                    return new_value.name.encode('utf-8')
                return ''
            else:
                return ''
        else:
            new_value = getattr(self.instance, self.from_field)

            if new_value:
                return new_value.name.encode('utf-8')
        return ''


class SubRegionMapping(IdentityMapping):
    """
    Map a sub-region name name or '' if no country set.
    """
    def map(self):
        # Check if the country is in a related object (e.g. 'address.country')
        if "." in self.from_field:
            obj, field = self.from_field.split('.')
            related = getattr(self.instance, obj, None)
            if related:
                country = getattr(related, field, '')
                if country:
                    return country.subregion.name.encode('utf-8')
                return ''
            else:
                return ''
        else:
            country = getattr(self.instance, self.from_field)

            if country:
                return country.subregion.name.encode('utf-8')
        return ''


class RegionMapping(IdentityMapping):
    """
    Map a region name name or '' if no country set.
    """
    def map(self):
        # Check if the country is in a related object (e.g. 'address.country')
        if "." in self.from_field:
            obj, field = self.from_field.split('.')
            related = getattr(self.instance, obj, None)
            if related:
                country = getattr(related, field, '')
                if country:
                    return country.subregion.region.name.encode('utf-8')
                return ''
            else:
                return ''
        else:
            country = getattr(self.instance, self.from_field)

            if country:
                return country.subregion.region.name.encode('utf-8')
        return ''


class RelatedObjectMapping(IdentityMapping):
    """
    Map to a related object id (to_csv) or Salesforce object (to_field).
    """

    def __init__(self, from_field=None, sf_model=None):
        self.sf_model = sf_model
        super(RelatedObjectMapping, self).__init__(from_field)

    def to_field(self):
        if "." in self.from_field:
            parts = self.from_field.split('.')

        related_id = getattr(self.instance, '{0}_id'.format(self.from_field))
        # Somtimes it somehow returns multiple objects.
        objs = self.sf_model.objects.filter(external_id=related_id).all()
        if objs.count():
            sf_object = objs[0]
            return sf_object
        return None

    def to_csv(self):
        related_id = self.get_field(self.instance, '{0}_id'.format(self.from_field))
        return related_id


class UserDonorMapping(IdentityMapping):
    """
    Map to a related object id (to_csv) or Salesforce object (to_field).
    """

    def __init__(self, from_field=None, sf_model=None):
        self.sf_model = sf_model
        super(UserDonorMapping, self).__init__(from_field)

    def to_field(self):
        order = getattr(self.instance, 'order')
        related_id = order.user_id
        if not related_id:
            return None

        # Somtimes it somehow returns multiple objects.
        objs = self.sf_model.objects.filter(external_id=related_id).all()
        if objs.count():
            sf_object = objs[0]
            return sf_object
        return None

    def to_csv(self):
        related_id = self.get_field(self.instance, '{0}_id'.format(self.from_field))
        return related_id


class OrderPaymentMethodMapping(StringMapping):
    """
    Returns the payment method based on an order
    """

    def map_value(self, old_value):
        order = super(StringMapping, self).map_value(old_value)
        lp = order.order_payments.order_by(created)[-1]
        if order and lp:
            new_value = lp.payment_method
            if(lp.payment_method.startswith("docdata")):
                new_value = lp.payment_method[7:]
            return new_value
        return self.default


class DonationStatusMapping(StringMapping):
    """
    Returns the payment method based on an order
    """

    def map(self):
        old_value = getattr(self.instance, 'order')
        new_value = self.map_value(old_value.get_status_display())
        return new_value
