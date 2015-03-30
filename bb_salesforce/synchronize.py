import csv
import os

from django.db import transaction

from bb_salesforce import models as sf_models
from bb_salesforce import transformers


def sync_model(model=None, logger=None, updated_after=None, only_new=False):

    sf_model = getattr(sf_models, "Salesforce{0}".format(model.__name__))
    transformer = getattr(transformers, "{0}Transformer".format(model.__name__))

    objects = model.objects
    if updated_after:
        objects = objects.filter(updated__gte=updated_after)

    logger.info("Found {0} {1}s".format(objects.count(), model.__name__))

    t = 0

    for obj in objects.all():
        t += 1
        logger.info("Syncing {0}  {1}/{2} [{3}] {4}".format(
            model.__name__, t, objects.count(), obj.id, str(obj)))
        trans_object = transformer().transform(obj)

        new = True
        try:
            sf_object = sf_model.objects.get(
                external_id=trans_object['external_id'])
            new = False
        except sf_model.DoesNotExist:
            sf_object  = sf_model(external_id=trans_object['external_id'])
        for attr, value in trans_object.iteritems():
            setattr(sf_object, attr, value)
        if (only_new and new) or not only_new:
            sf_object.save()

def sync_all(logger, updated_after=None, only_new=False):
    from bluebottle.organizations.models import Organization, OrganizationMember
    from bluebottle.members.models import Member
    from bluebottle.tasks.models import Task, TaskMember
    from bluebottle.donations.models import Donation
    from bluebottle.projects.models import Project, ProjectBudgetLine
    from bluebottle.fundraisers.models import Fundraiser

    sync_model(Member, logger, updated_after, only_new)
    sync_model(Organization, logger, updated_after, only_new)
    sync_model(OrganizationMember, logger, updated_after, only_new)
    sync_model(Project, logger, updated_after, only_new)
    sync_model(Fundraiser, logger, updated_after, only_new)
    sync_model(ProjectBudgetLine, logger, updated_after, only_new)
    sync_model(Task, logger, updated_after, only_new)
    sync_model(TaskMember, logger, updated_after, only_new)
    sync_model(Donation, logger, updated_after, only_new)


def export_model(model=None, logger=None, updated_after=None):

    objects = model.objects
    if updated_after:
        objects = objects.filter(updated__gte=updated_after)

    logger.info("Found {0} {1}s".format(objects.count(), model.__name__))

    t = 0

    filename = 'BLUE2SFDC_{0}.csv'.format(model.__name__)

    with open(os.path.join(path, filename), 'wb') as csv_outfile:
        csv_writer = csv.writer(csv_outfile, quoting=csv.QUOTE_ALL)

        # Header row
        csv_writer.writerow(self.field_map.keys())

        for obj in objects.all():
            t += 1
            logger.info("Syncing {0}  {1}/{2} [{3}] {4}".format(
                model.__name__, t, objects.count(), obj.id, str(obj)))
            trans_object = transformer().transform(obj)
            export_object = exporter().export(trans_object)
            csvwriter.writerow(export_object.to_csv())


def export_all(logger, updated_after=None):
    from bluebottle.organizations.models import Organization, OrganizationMember
    from bluebottle.members.models import Member
    from bluebottle.tasks.models import Task, TaskMember
    from bluebottle.donations.models import Donation
    from bluebottle.projects.models import Project, ProjectBudgetLine
    from bluebottle.fundraisers.models import Fundraiser

    export_model(Organization, logger, updated_after)
