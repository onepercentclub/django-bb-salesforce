import time
from datetime import datetime
from django.utils import timezone
from django.core.management.color import no_style
from django.db import connections
from django.db import transaction
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, ObjectDoesNotExist
from pytz.exceptions import AmbiguousTimeError
from .mappings import IdentityMapping

import logging
logger = logging.getLogger(__name__)


class BaseTransformer(object):

    external_id = 'external_id'

    def get_mapping(self, field):
        """
        Get the mapping object for the specified field from `field_mapping`.
        """
        mapping = self.field_mapping.get(field)

        if mapping == True:
            # True means just copy the field
            mapping = IdentityMapping()

        elif mapping == None:
            # None means: throw away the data
            mapping = NullMapping()

        elif isinstance(mapping, basestring):
            # A string can be passed to map to a different field
            mapping = IdentityMapping(mapping)

        elif isinstance(mapping, dict):
            # Instance maps a related object to a destination object
            mapping = RelatedObjectMapping(mapping)

        # By this time mapping should be a callable yielding a dict
        assert callable(mapping), u'No forward mapping defined for mapping %s' % mapping

        return mapping

    def transform(self, from_instance):
        value_dict = {}
        for field in self.field_mapping.iterkeys():
            # Get the mapping
            mapping = self.get_mapping(field)
            value_dict.update(mapping(from_instance, field))
        return value_dict


    def map_fields(self, from_instance, to_instance):
        """
        Copy all fields from one object to another.
        """

        for field in self.field_mapping.iterkeys():
            # Get the mapping
            mapping = self.get_mapping(field)

            # Ignore auto-updated fields as they're dealt with after the model is saved.
            if isinstance(mapping, AutoUpdatedDateTimeMapping):
                continue

            value_dict = mapping(from_instance, field)

            assert isinstance(value_dict, dict), \
                'Mapping %s returned %s instead of a dict.' % \
                    (mapping, value_dict)

            for (new_field, new_value) in value_dict.iteritems():
                assert isinstance(new_field, basestring)

                setattr(to_instance, new_field, new_value)

    def list_from(self):
        """
        Return an iterable with all objects to be mapped to the new model.
        """

        # Default is to return all objects
        return self.from_model.objects.using(self.from_db).all()

    def list_to(self):
        """
        Return an iterable with all the new objects that have been mapped
        from the old model.
        """

        # Default is to return all objects
        return self.to_model.objects.using(self.to_db).all()

    def get_to_correspondence(self, other_object):
        """
        Return the kwargs used for finding correspondence between one object
        and another. By default, correspondence by PK is used.
        """

        return {'pk': other_object.pk}

    def get_from_correspondence(self, other_object):
        """
        Return the kwargs used for finding correspondence between one object
        and another. By default, correspondence by PK is used.
        """

        return {'pk': other_object.pk}

    def get_to(self, from_instance):
        """
        Given an existing 'old' instance, return the corresponding 'new'
        instance or None if no corresponding object exists.
        """

        # Default is to look up by id
        try:
            correspondence_args = self.get_to_correspondence(from_instance)

            return self._list_to().get(**correspondence_args)

        except self.to_model.DoesNotExist:
            return None

    def get_from(self, to_instance):
        """
        Given an existing 'new' instance, return the corresponding 'old'
        instance or None if no corresponding object exists.
        """

        # Default is to look up by id
        try:
            correspondence_args = self.get_from_correspondence(to_instance)

            return self._list_from().get(**correspondence_args)

        except self.from_model.DoesNotExist:
            return None

    def migrate_single(self, from_instance, to_instance):
        """ Migrate a single object. """

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(u"Migrating '%s' to '%s'",
                from_instance.__repr__(), to_instance.__unicode__())

        self.map_fields(from_instance, to_instance)

    def _migrate_from(self, from_instance):
        to_instance = self.get_to(from_instance)

        # Not existing? Create one!
        if not to_instance:
            to_instance = self.to_model()

        self.migrate_single(from_instance, to_instance)

        self.pre_validate(from_instance, to_instance)

        # Validate the model
        # (before saving, to find any errors in a timely fashion)
        self.validate_single(to_instance)

        self.pre_save(from_instance, to_instance)

        # Save to the database
        to_instance.save(using=self.to_db)

        # Migrate auto updated datetimes.
        if hasattr(self, 'auto_updated_datetime_fields'):
            for from_field, to_field in self.auto_updated_datetime_fields:
                self.migrate_auto_updated_datetime(from_instance, to_instance, from_field, to_field)

        self.post_save(from_instance, to_instance)

        return to_instance
