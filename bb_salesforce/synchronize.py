from bluebottle.organizations.models import Organization
from bluebottle.members.models import Member
from bb_salesforce.models import SalesforceOrganization, SalesforceContact
from bb_salesforce.transformers import OrganizationTransformer


def sync_organizations():
    organizations = Organization.objects.all()

    trans = OrganizationTransformer()
    for org in organizations:
        trans_org = trans.transform(org)
        sf_org, created = SalesforceOrganization.objects.get_or_create(external_id=trans_org['external_id'])
        sf_org.update(trans_org)
        sf_org.save()

def sync_members():
    members = Member.objects.all()

    trans = MemberTransformer()
    for member in members:
        trans_member = trans.transform(member)
        sf_member, created = SalesforceContact.objects.get_or_create(external_id=trans_member['external_id'])
        sf_member.update(trans_member)
        sf_member.save()

def sync_all():
    sync_organizations()
    sync_members()
    print "Done!"
