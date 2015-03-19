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

    def map(self, instance, from_field):
        return ''


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

    def __init__(self, to_field=None, default=''):
        self.default = default
        super(StringMapping, self).__init__(to_field)

    def map_value(self, old_value):
        old_value = super(StringMapping, self).map_value(old_value)
        if not old_value:
            return self.default
        return old_value


class EmailMapping(StringMapping):
    """
    Identity mapping but for email returns '' if email not valid.
    """

    def __init__(self, to_field=None):
        super(StringMapping, self).__init__(to_field)

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

    def __init__(self, length, *args, **kwargs):
        self.length = length
        super(CropMapping, self).__init__(*args, **kwargs)

    def __repr__(self):
        return u"<%s: %d characters>" % (self.__class__.__name__, self.length)

    def map_value(self, old_value):
        old_value = super(CropMapping, self).map_value(old_value)
        return old_value[:self.length]


class ConcatenateMapping(StringMapping):
    """
    Concatenate (string) fields into one value.
    """

    def __init__(self, from_fields, concatenate_str=' ', *args, **kwargs):
        self.from_fields = from_fields
        self.concatenate_str = concatenate_str
        super(ConcatenateMapping, self).__init__(*args, **kwargs)

    def map(self, from_instance, to_field):
        values = []
        for field in self.from_fields:
            values.append(getattr(from_instance, field))
        new_value = self.concatenate_str.join(values)
        return {to_field: new_value}


class TagsMapping(StringMapping):
    """
    Turn tags into a comma seprated list
    """

    def __init__(self, to_field=None):
        super(StringMapping, self).__init__(to_field)

    def map_value(self, old_value):
        old_value = super(StringMapping, self).map_value(old_value)
        return ", ".join(old_value.all())


class ChoiceMapping(StringMapping):
    """
    Turn tags into a comma seprated list
    """

    def __init__(self, to_field=None, choices_list=None):
        self.choices_list = choices_list
        super(StringMapping, self).__init__(to_field)

    def map(self, from_instance, to_field):
        from_field = self.from_field
        if self.choices_list:
            old_value = str(getattr(from_instance, from_field))
            return self.choices_list.values[old_value].title()
        display_value = "get_{0}_display()".format(from_field)
        old_value = getattr(from_instance, display_value)
        return {to_field: old_value}

class CountryMapping(IdentityMapping):
    """
    Map a country name or '' if no country set.
    """

    def map_value(self, old_value):
        if old_value:
            return old_value.name
        return ''
