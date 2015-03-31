# -*- coding: utf-8 -*-

class FieldSerializer(object):

    def __call__(self, from_instance):
        """ Just wrap to a more verbose map function. """
        return self.from_native(from_instance)

    def __repr__(self):
        return u'<%s>' % self.__class__.__name__

    def __init__(self, from_field):
        self.from_field = from_field
        super(FieldSerializer, self).__init__()

    def from_native(self, from_instance):
        old_value = from_instance[self.from_field]
        return old_value


class BooleanSerializer(FieldSerializer):
    """
    Return boolean as integer
    """
    def from_native(self, from_instance):
        old_value = super(BooleanSerializer, self).from_native(from_instance)
        return int(old_value)


class UnicodeSerializer(FieldSerializer):
    """
    Return unicode as utf-8 strings.
    """
    def from_native(self, from_instance):
        old_value = super(UnicodeSerializer, self).from_native(from_instance)
        if isinstance(old_value, int):
            old_value = str(old_value)
        if isinstance(old_value, unicode):
            return old_value.encode('utf-8')
        else:
            return old_value


class DateSerializer(FieldSerializer):

    def __init__(self, from_field,
                 date_format="%Y-%m-%dT%H:%M:%S.000Z"):
        super(DateSerializer, self).__init__(from_field)
        self.date_format = date_format

    def from_native(self, from_instance):
        old_value = super(DateSerializer, self).from_native(from_instance)
        if old_value:
            return old_value.date().strftime(self.date_format)
        return ""


class EmptySerializer(FieldSerializer):
    """
    Return empty string. For removed fields.
    """
    def from_native(self, from_instance):
        return ""
