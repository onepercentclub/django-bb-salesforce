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

        'E_mail_address': EmailMapping('email'),
        'Phone': 'phone_number',
        'Website': 'website',
        # 'Twitter': 'twitter',
        'Facebook': 'facebook',
        'Skype': 'skype',
        'Tags': TagsMapping('tags'),

        'Organization_created_date': DateTimeMapping('created'),
        'Deleted': DateTimeMapping('deleted'),
    }


class MemberTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'Username': 'username',
        'Email': EmailMapping('email'),
        'Active': 'is_active',
        'Member_since': DateTimeMapping('date_joined'),
        'Date_Joined': DateTimeMapping('date_joined'),   # Duplicate
        'Deleted': DateTimeMapping('deleted'),

        'Category1': ChoiceMapping('user_type'),

        'FirstName':  'first_name',
        'LastName': StringMapping('last_name', default="Member"),

        'Location': 'place',

        'Picture_Location': ImageMapping('picture'),
        'About_me_us': StringMapping('about_me', omit_csv=True),               # Long text
        'Primary_language': 'primary_language',
        'Receive_newsletter': 'newsletter',
        'Phone': 'phone_number',
        'Birthdate': DateTimeMapping('birthdate'),
        'Gender': ChoiceMapping('gender'),

        'MailingCity': 'address.city',
        'MailingStreet': StreetMapping('address'),
        'MailingCountry': CountryMapping('address.country'),
        'MailingPostalCode': RelatedMapping('address.postal_code'),
        'MailingState': RelatedMapping('address.state'),

        'Has_Activated_Account': 'is_active',
        'Date_Last_Login': DateTimeMapping('last_login'),

        'Account_city': RelatedMapping('monthlydonor.city'),
        'Account_IBAN': RelatedMapping('monthlydonor.iban'),
        'Account_holder': RelatedMapping('monthlydonor.name'),
        'Account_Active_Recurring_Debit': RelatedMapping('monthlydonor.active'),

        'Website':  'website',
        'Facebook':  'facebook',
        'Twitter': 'twitter',
        'Skype': 'skypename'
    }


class OrganizationMemberTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'Contact': RelatedObjectMapping('user', SalesforceMember),
        'Organization':
            RelatedObjectMapping('organization', SalesforceOrganization),
        'Role': 'function'
    }


class ProjectTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'Project_name': 'title',
        'Describe_the_project_in_one_sentence': CropMapping('pitch', 5000, omit_csv=True),      # Long text
        'VideoURL': 'video_url',
        'Is_Campaign': 'is_campaign',

        'Amount_at_the_moment': EuroMapping('amount_donated'),
        'Amount_requested': EuroMapping('amount_asked'),
        'Amount_still_needed': EuroMapping('amount_needed'),
        'Donation_total':  EuroMapping('amount_donated'),
        'Donation_oo_total':  EuroMapping('amount_donated'),
        'Amount_extra': EuroMapping('amount_extra'),

        'Allow_Overfunding': 'allow_overfunding',
        'Story': StringMapping('story', omit_csv=True),                                          # Long text
        'Popularity': 'popularity',
        'Skip_Monthly': 'skip_monthly',

        'Picture_Location': ImageMapping('image'),

        'Date_project_deadline': DateTimeMapping('deadline'),
        'Project_created_date': DateTimeMapping('created'),
        'Project_updated_date': DateTimeMapping('updated'),
        'Date_plan_submitted': DateTimeMapping('date_submitted'),
        'Date_Started': DateTimeMapping('campaign_started'),
        'Date_Ended': DateTimeMapping('campaign_ended'),
        'Date_Funded': DateTimeMapping('campaign_funded'),

        'Country_in_which_the_project_is_located': CountryMapping('country'),
        'Country': RelatedObjectMapping('country', SalesforceCountry),
        'Sub_region': SubRegionMapping('country'),
        'Region': RegionMapping('country'),
        'Theme': RelatedMapping('theme.name'),
        'Status_project': RelatedMapping('status.name'),
        'NumberOfPeopleReachedDirect': 'reach',
        'Language': RelatedMapping('language.language_name'),
        'Type': 'project_type',
        'Slug': 'slug',

        'Supporter_count': MethodMapping('supporter_count'),
        'Supporter_oo_count': MethodMapping('supporter_count', True),

        'Project_Owner': RelatedObjectMapping('owner', SalesforceMember),
        'Organization':
            RelatedObjectMapping('organization', SalesforceOrganization),

    }


class FundraiserTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'Owner': RelatedObjectMapping('owner', SalesforceMember),
        'Project': RelatedObjectMapping('project', SalesforceProject),
        'Picture_Location':  ImageMapping('image'),
        'Name': CropMapping('title', 80),
        'Description': StringMapping('description', omit_csv=True),                              # Long text
        'VideoURL': 'video_url',
        'Amount':  EuroMapping('amount'),
        'Amount_at_the_moment': EuroMapping('amount_donated'),
        'Deadline': DateTimeMapping('deadline'),
        'Created': DateTimeMapping('created'),
    }


class ProjectBudgetLineTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'Costs':  EuroCentMapping('amount'),
        'Description': StringFlatMapping('description'),
        'Project': RelatedObjectMapping('project', SalesforceProject)
    }


class DonationTransformer(BaseTransformer):
    
    field_mapping = {

        'external_id': 'id',
        'Amount': EuroMapping('amount'),

        'Receiver': UserDonorMapping('order.user', SalesforceMember),
        'Project': RelatedObjectMapping('project', SalesforceProject),
        'Fundraiser': RelatedObjectMapping('fundraiser', SalesforceFundraiser),

        'StageName': DonationStatusMapping('order'),

        'CloseDate': DateTimeMapping('created'),
        'Donation_created_date': DateTimeMapping('created'),
        'Donation_updated_date': DateTimeMapping('updated'),
        'Donation_ready_date': DateTimeMapping('completed'),

        'Type': RelatedMapping('order.order_type'),
        'Name': UserOrAnonymousMapping('user'),
        'RecordTypeId': StaticMapping('012A0000000ZK6FIAW'),
        'Payment_method': OrderPaymentMethodMapping('order', 'Unknown')
    }


class TaskTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'Project': RelatedObjectMapping('project', SalesforceProject),
        'Author':  RelatedObjectMapping('author', SalesforceMember),
        'Deadline': DateTimeMapping('deadline'),

        'Effort': 'time_needed',
        'Extended_task_description': StringMapping('description', omit_csv=True),          # Long text
        'Location_of_the_task': 'location',
        'People_Needed': 'people_needed',
        'End_Goal': StringMapping('end_goal', omit_csv=True),                              # Long text

        'Task_expertise': RelatedMapping('skill.name'),

        'Task_status': 'status',
        'Title': 'title',
        'Task_created_date': DateTimeMapping('created'),
        'Tags': TagsMapping('tags'),
        'Date_realized': DateTimeMapping('date_realized'),
    }


class TaskMemberTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'Contacts': RelatedObjectMapping('member', SalesforceMember),
        'X1_CLUB_Task': RelatedObjectMapping('task', SalesforceTask),
        'Motivation': StringMapping('motivation', omit_csv=True),                 # Long text
        'Status': ChoiceMapping('status'),
        'Taskmember_Created_Date': DateTimeMapping('created')
    }
