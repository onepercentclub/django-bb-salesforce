# -*- coding: utf-8 -*-

import csv
import os

from django.utils import timezone
from django.conf import settings

from bb_salesforce import models as sf_models
from bb_salesforce.models import SalesforceLogItem
from bb_salesforce import transformers


def sync_model(model=None, logger=None, updated_after=None, only_new=False, sync_counter=None, updated_field='updated',
               updated_search='gte'):

    sf_model_name = "Salesforce{0}".format(model.__name__)
    sf_model = getattr(sf_models, sf_model_name)

    transformer_name = "{0}Transformer".format(model.__name__)
    transformer = getattr(transformers, transformer_name)

    objects = model.objects
    if updated_after:
        search_filter = '{0}__{1}'.format(updated_field, updated_search)
        objects = objects.filter(**{search_filter: updated_after})

    logger.info("Synchronizing {0} {1}s".format(objects.count(), model.__name__))
    t = 0

    for obj in objects.all():
        t += 1
        logger.debug("Syncing {0}  {1}/{2} [{3}] {4}".format(
            model.__name__, t, objects.count(), obj.id, str(obj)))

        trans_object = transformer(obj).to_dict()

        new = True
        try:
            sf_object = sf_model.objects.get(
                external_id=trans_object['external_id'])
            new = False
        except sf_model.DoesNotExist:
            logger.debug("Does not exist, assuming new record")
            sf_object = sf_model(external_id=trans_object['external_id'])
        except Exception as e:
            logger.error("Error while loading object id {0} - stopping: ".format(trans_object['external_id'] + str(e)))
            sync_counter.update('e')
            return

        for attr, value in trans_object.iteritems():
            setattr(sf_object, attr, value)
        if (only_new and new) or not only_new:
            try:
                sf_object.save()
                sync_counter.update('s')
            except Exception as e:
                sync_counter.update('e')
                logger.error("Error while saving object id {0}: ".format(trans_object['external_id']) + str(e))

    return


def sync_all(sync_counter, logger, updated_after=None, only_new=False):

    from bluebottle.organizations.models import Organization, OrganizationMember
    from bluebottle.members.models import Member
    from bluebottle.tasks.models import Task, TaskMember
    from bluebottle.donations.models import Donation
    from bluebottle.projects.models import Project, ProjectBudgetLine
    from bluebottle.fundraisers.models import Fundraiser

    sync_model(Member, logger, updated_after, only_new, sync_counter)
    sync_model(Organization, logger, updated_after, only_new, sync_counter)
    sync_model(OrganizationMember, logger, updated_after, only_new, sync_counter)
    sync_model(Project, logger, updated_after, only_new, sync_counter)
    sync_model(Fundraiser, logger, updated_after, only_new, sync_counter)
    sync_model(ProjectBudgetLine, logger, updated_after, only_new, sync_counter)
    sync_model(Task, logger, updated_after, only_new, sync_counter)
    sync_model(TaskMember, logger, updated_after, only_new, sync_counter)
    sync_model(Donation, logger, updated_after, only_new, sync_counter, 'order__updated')


def export_model(model=None, logger=None, updated_after=None, updated_field='updated',
                 updated_search='gte'):

    export_path = os.path.join(settings.PROJECT_ROOT, "export", "salesforce")
    transformer_name = "{0}Transformer".format(model.__name__)
    transformer = getattr(transformers, transformer_name)
    sf_model_name = "Salesforce{0}".format(model.__name__)
    sf_model = getattr(sf_models, sf_model_name)

    objects = model.objects
    if updated_after:
        search_filter = '{0}__{1}'.format(updated_field, updated_search)
        objects = objects.filter(**{search_filter: updated_after})

    logger.info("Exporting {0} {1}s".format(objects.count(), model.__name__))

    t = 0

    filename = 'BLUE2SFDC_{0}s.csv'.format(model.__name__)
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    with open(os.path.join(export_path, filename), 'wb') as csv_outfile:
        csv_writer = csv.writer(csv_outfile, quoting=csv.QUOTE_ALL)

        # Get titles from db_column names from sf model
        sf_names = []
        for field in transformer.field_mapping.keys():
            local_name, sf_name = sf_model._meta.get_field_by_name(field)[0].get_attname_column()
            sf_names.append(sf_name)
        csv_writer.writerow(sf_names)

        for obj in objects.all():
            t += 1
            logger.debug("Exporting {0}  {1}/{2} [{3}] {4}".format(
                model.__name__, t, objects.count(), obj.id, str(obj)))
            export_row = transformer(obj).to_csv()
            csv_writer.writerow(export_row)


def export_all(logger, updated_after=None):
    from bluebottle.organizations.models import Organization, OrganizationMember
    from bluebottle.members.models import Member
    from bluebottle.tasks.models import Task, TaskMember
    from bluebottle.donations.models import Donation
    from bluebottle.projects.models import Project, ProjectBudgetLine
    from bluebottle.fundraisers.models import Fundraiser

    export_model(Member, logger, updated_after)
    export_model(Organization, logger, updated_after)
    export_model(OrganizationMember, logger, updated_after)
    export_model(Project, logger, updated_after)
    export_model(ProjectBudgetLine, logger, updated_after)
    export_model(Fundraiser, logger, updated_after)
    export_model(Task, logger, updated_after)
    export_model(TaskMember, logger, updated_after)
    export_model(Donation, logger, updated_after, 'order__updated')


def send_log(filename, errors, successes, command, command_ext, logger):
    sflog = SalesforceLogItem()
    logger.info("Sending log to Salesforce...")
    sflog.Entered__c = timezone.localtime(timezone.now())
    sflog.Source__c = str(command)
    sflog.Source_Extended__c = str(command_ext)
    sflog.Errors__c = errors
    sflog.Successes__c = successes

    with open(filename, "r") as logfile:
        for line in logfile:
            sflog.Message__c += line[:1300]

    try:
        sflog.save()
    except Exception as e:
        logger.error("Error while saving log: " + str(e))
