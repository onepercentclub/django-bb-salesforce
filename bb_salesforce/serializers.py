class FieldSerializer(object):

    def __init__(self, from_instance, from_field):
        self.from_instance = from_instance
        self.from_field = from_field

    def from_native(self):
        old_value = self.from_instance[self.from_field]
        return old_value


class UnicodeField(FieldSerializer):

    def from_native(self):
        old_value = super(UnicodeField, self).from_native()
        return old_value.encode('utf-8')


class DateField(FieldSerializer):

    def __init__(self, from_instance, from_field,
                 date_format="%Y-%m-%dT%H:%M:%S.000Z"):
        super(DateField, self).__init__(from_instance, from_field)
        self.date_format = date_format

    def from_native(self):
        old_value = super(DateField, self).from_native()
        return old_value.date().strftime(self.date_format)
