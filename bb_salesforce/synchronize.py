from bb_salesforce.models import (
    SalesforceOrganization, SalesforceContact, SalesforceProject,
    SalesforceFundraiser
)
from bb_salesforce.transformers import (
    OrganizationTransformer, MemberTransformer, ProjectTransformer,
    FundraiserTransformer
)


def sync_model(model=None, sf_model=None, transformer=None,
               logger=None, updated_after=None):

    objects = model.objects
    if updated_after:
        objects = objects.filter(updated__gte=updated_after)

    logger.info("Found {0} {1}s".format(objects.count(), model.__name__))

    t = 0
    for obj in objects.all():
        t += 1
        logger.info("Syncing {0}  {1}/{2} [ID={3}] {4}".format(
            model.__name__, t, objects.count(), obj.id, str(obj)))
        trans_object = transformer().transform(obj)

        try:
            sf_object = sf_model.objects.get(
                external_id=trans_object['external_id'])
        except sf_model.DoesNotExist:
            sf_object  = sf_model(external_id=trans_object['external_id'])
        for attr, value in trans_object.iteritems():
            setattr(sf_object, attr, value)
        sf_object.save()


def sync_all(logger, updated_after=None):
    from bluebottle.organizations.models import Organization, OrganizationMember
    from bluebottle.members.models import Member
    from bluebottle.tasks.models import Task, TaskMember
    from bluebottle.donations.models import Donation
    from bluebottle.projects.models import Project, ProjectBudgetLine
    from bluebottle.fundraisers.models import Fundraiser

    sync_model(Member, SalesforceContact,
               MemberTransformer,
               logger, updated_after)

    sync_model(Organization, SalesforceOrganization,
               OrganizationTransformer,
               logger, updated_after)

    sync_model(OrganizationMember, SalesforceOrganizationMember,
               OrganizationMemberTransformer,
               logger, updated_after)

    sync_model(Project, SalesforceProject,
               ProjectTransformer,
               logger, updated_after)

    sync_model(Fundraiser, SalesforceFundraiser,
               FundraiserTransformer,
               logger, updated_after)

    sync_model(ProjectBudgetLine, SalesforceProjectBudget,
               ProjectBudgetTransformer,
               logger, updated_after)

    sync_model(Task, SalesforceTask,
               TaskTransformer,
               logger, updated_after)

    sync_model(TaskMember, SalesforceTaskMember,
               TaskMemberTransformer,
               logger, updated_after)

    sync_model(Donation, SalesforceDonation,
               DonationTransformer,
               logger, updated_after)

    print "Done!"
