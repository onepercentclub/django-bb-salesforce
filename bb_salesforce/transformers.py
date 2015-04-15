from bb_salesforce.mappings import (
    CropMapping, StringMapping, CountryMapping,
    ConcatenateMapping, EmailMapping, TagsMapping,
    ChoiceMapping, EmptyMapping, RelatedMapping, StreetMapping, ImageMapping,
    SubRegionMapping, RegionMapping,DateTimeMapping, EuroMapping, EuroCentMapping, MethodMapping,
    RelatedObjectMapping, DateMapping, UserOrAnonymousMapping,
    StaticMapping, DonationStatusMapping,
    OrderPaymentMethodMapping)
from .base import BaseTransformer
from bb_salesforce.models import (
    SalesforceMember, SalesforceOrganization, SalesforceProject,
    SalesforceTask, SalesforceFundraiser)


class OrganizationTransformer(BaseTransformer):

    field_mapping = {
        'Organization_External_ID__c': 'id',
        'Name': StringMapping('name', default="Organization"),
        'BillingCity': CropMapping('city', 40),
        'BillingStreet': ConcatenateMapping(['address_line1', 'address_line2']),
        'BillingPostalCode': 'postal_code',
        'BillingState': CropMapping('state', 20),
        'BillingCountry': CountryMapping('country'),

        'E_mail_address__c': EmailMapping('email'),
        'Phone': 'phone_number',
        'Website': 'website',
        'Twitter__c': 'twitter',
        'Facebook__c': 'facebook',
        'Skype__c': 'skype',
        'Tags__c': TagsMapping('tags'),
        'Bank_account_name__c': 'account_holder_name',

        'Bank_account_address__c': 'account_holder_address',
        'Bank_account_postalcode__c': 'account_holder_postal_code',
        'Bank_account_city__c': 'account_holder_city',
        'Bank_account_country__c':  CountryMapping('account_holder_country'),

        'Bank_bankname__c':  'account_bank_name',
        'Bank_address__c': 'account_bank_address',
        'Bank_postalcode__c': 'account_bank_postal_code',
        'Bank_city__c': 'account_bank_city',
        'Bank_country__c': CountryMapping('account_bank_country'),

        'Bank_account_number__c': 'account_number',
        'Bank_SWIFT__c': 'account_bic',
        'Bank_account_IBAN__c': 'account_iban',
        'Organization_created_date__c': DateTimeMapping('created'),
        'Deleted__c': DateTimeMapping('deleted'),
    }


class MemberTransformer(BaseTransformer):

    field_mapping = {
        'Contact_External_ID__c': 'id',
        'Username__c': 'username',
        'Email': EmailMapping('email'),
        'Active__c': 'is_active',
        'Member_since__c': DateTimeMapping('date_joined'),
        'Date_Joined__c': DateTimeMapping('date_joined'),   # Duplicate
        'Deleted__c': DateTimeMapping('deleted'),

        'Category1__c': ChoiceMapping('user_type'),

        'FirstName':  'first_name',
        'LastName': StringMapping('last_name', default="Member"),

        'Location__c': 'location',
        'Picture_Location__c': ImageMapping('picture'),
        # 'About_me_us__c': 'about_me',
        'Primary_language__c': 'primary_language',
        'Receive_newsletter__c': 'newsletter',
        'Phone': 'phone_number',
        'Birthdate': DateTimeMapping('birthdate'),
        
        'Gender__c': ChoiceMapping('gender'),

        'MailingCity': 'address.city',
        'MailingStreet': StreetMapping('address'),

        'MailingCountry': CountryMapping('address.country'),
        'MailingPostalCode': RelatedMapping('address.postal_code'),
        'MailingState': RelatedMapping('address.state'),

        'Has_Activated_Account__c': 'is_active',
        'Date_Last_Login__c': DateTimeMapping('last_login'),

        'Account_city__c': RelatedMapping('monthlydonor.city'),
        'Account_IBAN__c': RelatedMapping('monthlydonor.iban'),
        'Account_holder__c': RelatedMapping('monthlydonor.name'),
        'Account_Active_Recurring_Debit__c':
            RelatedMapping('monthlydonor.active'),

        'Website__c':  'website',
        'Facebook__c':  'facebook',

        # Removed fields
        # 'why_one_percent_member':  NullMapping(),
        # 'availability':  NullMapping(),
        # 'twitter':  NullMapping(),
        # 'skype':  NullMapping(),
        # 'tags': NullMapping(),
    }


class OrganizationMemberTransformer(BaseTransformer):

    field_mapping = {
        'Organization_Member_External_Id__c': 'id',
        'Contact__c': RelatedObjectMapping('user', SalesforceMember),
        'Organization__c':
            RelatedObjectMapping('organization', SalesforceOrganization),
        'Role__c': 'function'
    }


class ProjectTransformer(BaseTransformer):

    field_mapping = {

        'Project_External_ID__c': 'id',
        'Project_name__c': 'title',
        # 'Describe_the_project_in_one_sentence__c': CropMapping('pitch', 5000),
        'VideoURL__c': 'video_url',
        'Is_Campaign__c': 'is_campaign',

        'Amount_at_the_moment__c': EuroMapping('amount_donated'),
        'Amount_requested__c': EuroMapping('amount_asked'),
        'Amount_still_needed__c': EuroMapping('amount_needed'),
        'Donation_total__c':  EuroMapping('amount_donated'),
        'Donation_oo_total__c':  EuroMapping('amount_donated'),

        'Allow_Overfunding__c': 'allow_overfunding',
        # 'Story__c': 'story',

        'Picture_Location__c': ImageMapping('image'),

        'Date_project_deadline__c': DateTimeMapping('deadline'),
        'Project_created_date__c': DateTimeMapping('created'),
        'Project_updated_date__c': DateTimeMapping('updated'),
        'Date_plan_submitted__c': DateTimeMapping('date_submitted'),
        'Date_Started__c': DateTimeMapping('campaign_started'),
        'Date_Ended__c': DateTimeMapping('campaign_ended'),
        'Date_Funded__c': DateTimeMapping('campaign_funded'),

        'Country_in_which_the_project_is_located__c': CountryMapping('country'),
        'Sub_region__c': SubRegionMapping('country'),
        'Region__c': RegionMapping('country'),
        'Theme__c': RelatedMapping('theme.name'),
        'Status_project__c': RelatedMapping('status.name'),

        'Tags__c': TagsMapping('tags'),
        'Partner_Organization__c': RelatedMapping('partner_organization.name', default="-"),

        'Slug__c': 'slug',
        'Supporter_count__c': MethodMapping('supporters_count'),
        'Supporter_oo_count__c': MethodMapping('supporters_count', True),

        'Project_Owner__c': RelatedObjectMapping('owner', SalesforceMember),
        'Organization__c':
            RelatedObjectMapping('organization', SalesforceOrganization),

    }


class FundraiserTransformer(BaseTransformer):

    field_mapping = {
        'Fundraiser_External_ID__c': 'id',
        'Owner__c': RelatedObjectMapping('owner', SalesforceMember),
        'Project__c': RelatedObjectMapping('project', SalesforceProject),
        'Picture_Location__c':  ImageMapping('image'),
        # 'Picture_Location__c': EmptyMapping('image'),
        'Name': CropMapping('title', 80),
        # 'Name': EmptyMapping('name'),
        # 'Description__c': 'description',
        'VideoURL__c': 'video_url',
        # 'VideoURL__c': EmptyMapping('video_url'),
        'Amount__c':  EuroMapping('amount'),
        'Amount_at_the_moment__c': EuroMapping('amount_donated'),
        'Deadline__c': DateTimeMapping('deadline'),
        'Created__c': DateTimeMapping('created'),
    }


class ProjectBudgetLineTransformer(BaseTransformer):

    field_mapping = {
        'Project_Budget_External_ID__c': 'id',
        'Costs__c':  EuroCentMapping('amount'),
        'Description__c': 'description',
        'Project__c': RelatedObjectMapping('project', SalesforceProject)
    }


class DonationTransformer(BaseTransformer):
    
    field_mapping = {

        'external_id_donation': 'id',
        'amount': EuroMapping('amount'),

        'donor': RelatedObjectMapping('order.user', SalesforceMember),
        'project': RelatedObjectMapping('project', SalesforceProject),
        'fundraiser':
            RelatedObjectMapping('fundraiser', SalesforceFundraiser),

        'stage_name': DonationStatusMapping('order'),

        'close_date': DateTimeMapping('created'),
        'donation_created_date': DateTimeMapping('created'),
        'donation_updated_date': DateTimeMapping('updated'),
        'donation_ready_date': DateTimeMapping('completed'),

        'type': RelatedMapping('order.order_type'),
        'name': UserOrAnonymousMapping('user'),
        'record_type': StaticMapping('012A0000000ZK6FIAW'),
        'payment_method': OrderPaymentMethodMapping('order')

    }


class TaskTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'project': RelatedObjectMapping('project', SalesforceProject),
        'author':  RelatedObjectMapping('author', SalesforceMember),
        'deadline': DateTimeMapping('deadline'),

        'effort': 'time_needed',
        # 'extended_task_description': 'description',
        'location_of_the_task': 'location',
        'people_needed': 'people_needed',
        # 'end_goal': 'end_goal',

        'task_expertise': RelatedMapping('skill.name'),

        'task_status': 'status',
        'title': 'title',
        'task_created_date': DateTimeMapping('created'),
        'tags': TagsMapping('tags'),
        'date_realized': DateTimeMapping('date_realized'),
    }


class TaskMemberTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'contacts': RelatedObjectMapping('member', SalesforceMember),
        'x1_club_task': RelatedObjectMapping('task', SalesforceTask),
        # 'motivation': 'motivation',
        'status': ChoiceMapping('status'),
        'taskmember_created_date': DateTimeMapping('created')
    }
