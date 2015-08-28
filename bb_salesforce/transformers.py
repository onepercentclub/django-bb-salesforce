from bb_salesforce.mappings import (
    CropMapping, StringMapping, CountryMapping,
    ConcatenateMapping, EmailMapping, TagsMapping,
    ChoiceMapping, EmptyMapping, RelatedMapping, StreetMapping, ImageMapping,
    SubRegionMapping, RegionMapping,DateTimeMapping, EuroMapping, EuroCentMapping, MethodMapping,
    RelatedObjectMapping, DateMapping, UserOrAnonymousMapping, StringReplaceMapping,
    StaticMapping, DonationStatusMapping,
    OrderPaymentMethodMapping, UserDonorMapping, StringFlatMapping)
from .base import BaseTransformer
from bb_salesforce.models import (
    SalesforceMember, SalesforceOrganization, SalesforceProject,
    SalesforceTask, SalesforceFundraiser, SalesforceCountry)


class OrganizationTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'Name': StringMapping('name', default="Organization"),
        'BillingCity': CropMapping('city', 40),
        'BillingStreet': ConcatenateMapping(['address_line1', 'address_line2']),
        'BillingPostalCode': 'postal_code',
        'BillingState': CropMapping('state', 20),
        'BillingCountry': CountryMapping('country'),

        'E_mail_address__c': EmailMapping('email'),
        'Phone': 'phone_number',
        'Website': 'website',
        # 'Twitter__c': 'twitter',
        'Facebook__c': 'facebook',
        'Skype__c': 'skype',
        'Tags__c': TagsMapping('tags'),

        'Organization_created_date__c': DateTimeMapping('created'),
        'Deleted__c': DateTimeMapping('deleted'),
    }


class MemberTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'Username__c': 'username',
        'Email': EmailMapping('email'),
        'Active__c': 'is_active',
        'Member_since__c': DateTimeMapping('date_joined'),
        'Date_Joined__c': DateTimeMapping('date_joined'),   # Duplicate
        'Deleted__c': DateTimeMapping('deleted'),

        'Category1__c': ChoiceMapping('user_type'),

        'FirstName':  'first_name',
        'LastName': StringMapping('last_name', default="Member"),

        'Location__c': 'place',

        'Picture_Location__c': ImageMapping('picture'),
        'About_me_us__c': StringMapping('about_me', omit_csv=True),               # Long text
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
        'Twitter__c': 'twitter',
        'Skype__c': 'skypename'
    }


class OrganizationMemberTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'Contact__c': RelatedObjectMapping('user', SalesforceMember),
        'Organization__c':
            RelatedObjectMapping('organization', SalesforceOrganization),
        'Role__c': 'function'
    }


class ProjectTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'Project_name__c': 'title',
        'Describe_the_project_in_one_sentence__c': CropMapping('pitch', 5000, omit_csv=True),      # Long text
        'VideoURL__c': 'video_url',
        'Is_Campaign__c': 'is_campaign',

        'Amount_at_the_moment__c': EuroMapping('amount_donated'),
        'Amount_requested__c': EuroMapping('amount_asked'),
        'Amount_still_needed__c': EuroMapping('amount_needed'),
        'Donation_total__c':  EuroMapping('amount_donated'),
        'Donation_oo_total__c':  EuroMapping('amount_donated'),
        'Amount_extra__c': EuroMapping('amount_extra'),

        'Allow_Overfunding__c': 'allow_overfunding',
        'Story__c': StringMapping('story', omit_csv=True),                                          # Long text
        'Popularity__c': 'popularity',
        'Skip_Monthly__c': 'skip_monthly',

        'Picture_Location__c': ImageMapping('image'),

        'Date_project_deadline__c': DateTimeMapping('deadline'),
        'Project_created_date__c': DateTimeMapping('created'),
        'Project_updated_date__c': DateTimeMapping('updated'),
        'Date_plan_submitted__c': DateTimeMapping('date_submitted'),
        'Date_Started__c': DateTimeMapping('campaign_started'),
        'Date_Ended__c': DateTimeMapping('campaign_ended'),
        'Date_Funded__c': DateTimeMapping('campaign_funded'),

        'Country_in_which_the_project_is_located__c': CountryMapping('country'),
        'Country__c': RelatedObjectMapping('country', SalesforceCountry),
        'Sub_region__c': SubRegionMapping('country'),
        'Region__c': RegionMapping('country'),
        'Theme__c': RelatedMapping('theme.name'),
        'Status_project__c': RelatedMapping('status.name'),
        'NumberOfPeopleReachedDirect__c': 'reach',
        'Language__c': RelatedMapping('language.language_name'),

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
        'external_id': 'id',
        'Owner__c': RelatedObjectMapping('owner', SalesforceMember),
        'Project__c': RelatedObjectMapping('project', SalesforceProject),
        'Picture_Location__c':  ImageMapping('image'),
        'Name': CropMapping('title', 80),
        'Description__c': StringMapping('description', omit_csv=True),                              # Long text
        'VideoURL__c': 'video_url',
        'Amount__c':  EuroMapping('amount'),
        'Amount_at_the_moment__c': EuroMapping('amount_donated'),
        'Deadline__c': DateTimeMapping('deadline'),
        'Created__c': DateTimeMapping('created'),
    }


class ProjectBudgetLineTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'Costs__c':  EuroCentMapping('amount'),
        'Description__c': StringFlatMapping('description'),
        'Project__c': RelatedObjectMapping('project', SalesforceProject)
    }


class DonationTransformer(BaseTransformer):
    
    field_mapping = {

        'external_id': 'id',
        'Amount': EuroMapping('amount'),

        'Receiver__c': UserDonorMapping('order.user', SalesforceMember),
        'Project__c': RelatedObjectMapping('project', SalesforceProject),
        'Fundraiser__c': RelatedObjectMapping('fundraiser', SalesforceFundraiser),

        'StageName': DonationStatusMapping('order'),

        'CloseDate': DateTimeMapping('created'),
        'Donation_created_date__c': DateTimeMapping('created'),
        'Donation_updated_date__c': DateTimeMapping('updated'),
        'Donation_ready_date__c': DateTimeMapping('completed'),

        'Type': RelatedMapping('order.order_type'),
        'Name': UserOrAnonymousMapping('user'),
        'RecordTypeId': StaticMapping('012A0000000ZK6FIAW'),
        'Payment_method__c': OrderPaymentMethodMapping('order', 'Unknown')
    }


class TaskTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'Project__c': RelatedObjectMapping('project', SalesforceProject),
        'Author__c':  RelatedObjectMapping('author', SalesforceMember),
        'Deadline__c': DateTimeMapping('deadline'),

        'Effort__c': 'time_needed',
        'Extended_task_description__c': StringMapping('description', omit_csv=True),          # Long text
        'Location_of_the_task__c': 'location',
        'People_Needed__c': 'people_needed',
        'End_Goal__c': StringMapping('end_goal', omit_csv=True),                              # Long text

        'Task_expertise__c': RelatedMapping('skill.name'),

        'Task_status__c': 'status',
        'Title__c': 'title',
        'Task_created_date__c': DateTimeMapping('created'),
        'Tags__c': TagsMapping('tags'),
        'Date_realized__c': DateTimeMapping('date_realized'),
    }


class TaskMemberTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'Contacts__c': RelatedObjectMapping('member', SalesforceMember),
        'X1_CLUB_Task__c': RelatedObjectMapping('task', SalesforceTask),
        'Motivation__c': StringMapping('motivation', omit_csv=True),                 # Long text
        'Status__c': ChoiceMapping('status'),
        'Taskmember_Created_Date__c': DateTimeMapping('created')
    }
