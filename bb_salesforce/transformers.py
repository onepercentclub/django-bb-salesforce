from bb_salesforce.mappings import (
    CropMapping, StringMapping, CountryMapping,
    ConcatenateMapping, EmailMapping, TagsMapping,
    ChoiceMapping, EmptyMapping, RelatedMapping, StreetMapping, ImageMapping,
    SubRegionMapping, RegionMapping,DateTimeMapping, EuroMapping, MethodMapping,
    RelatedObjectMapping, DateMapping, UserOrAnonymousMapping,
    StaticMapping, DonationStatusMapping,
    OrderPaymentMethodMapping)
from .base import BaseTransformer
from bb_salesforce.models import (
    SalesforceMember, SalesforceOrganization, SalesforceProject,
    SalesforceTask, SalesforceFundraiser)


class OrganizationTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'name': 'name',
        'billing_city': CropMapping('city', 40),
        'billing_street': ConcatenateMapping(['address_line1',
                                              'address_line2']),

        'billing_postal_code': 'postal_code',
        'billing_state': CropMapping('state', 20),
        'billing_country': CountryMapping('country'),

        'email': EmailMapping('email'),
        'phone': 'phone_number',
        'website': 'website',
        'twitter': 'twitter',
        'facebook': 'facebook',
        'skype': 'skype',
        'tags': TagsMapping('tags'),
        'bank_account_name': 'account_holder_name',

        'bank_account_address': 'account_holder_address',
        'bank_account_postalcode': 'account_holder_postal_code',
        'bank_account_city': 'account_holder_city',
        'bank_account_country':  CountryMapping('account_holder_country'),

        'bank_name':  'account_bank_name',
        'bank_address': 'account_bank_address',
        'bank_postalcode': 'account_bank_postal_code',
        'bank_city': 'account_bank_city',
        
        'account_bank_country': CountryMapping('account_bank_country'),

        'bank_account_number': 'account_number',
        'bank_bic_swift': 'account_bic',
        'bank_account_iban': 'account_iban',
        'created_date': 'created',
        'deleted_date': 'deleted',
    }


class MemberTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'user_name': 'username',
        'email': EmailMapping('email'),
        'is_active': 'is_active',
        'member_since': 'date_joined',
        'date_joined': 'date_joined',
        'deleted': 'deleted',

        'contact.category1': ChoiceMapping('user_type'),

        'first_name':  'first_name',
        'last_name': StringMapping('last_name', default="Member"),

        'location': 'location',
        'picture_location': ImageMapping('picture'),
        'about_me_us': 'about_me',
        'primary_language': 'primary_language',
        'receive_newsletter': 'newsletter',
        'phone': 'phone_number',
        'birth_date': 'birthdate',
        
        'gender': ChoiceMapping('gender'),

        'mailing_city': 'address.city',
        'mailing_street': StreetMapping('address'),

        'mailing_country': CountryMapping('address.country'),
        'mailing_postal_code': RelatedMapping('address.postal_code'),
        'mailing_state': RelatedMapping('address.state'),

        'has_activated': 'is_active',
        'last_login': 'last_login',

        'bank_account_city': RelatedMapping('monthlydonor.city'),
        'bank_account_iban': RelatedMapping('monthlydonor.iban'),
        'bank_account_holder': RelatedMapping('monthlydonor.name'),
        'bank_account_active_recurring_debit':
            RelatedMapping('monthlydonor.active'),

        # Removed fields

        # 'bank_account_number':  NullMapping(),
        # 'website':  NullMapping(),
        # 'why_one_percent_member':  NullMapping(),
        # 'availability':  NullMapping(),
        # 'facebook':  NullMapping(),
        # 'twitter':  NullMapping(),
        # 'skype':  NullMapping(),
        # 'tags': NullMapping(),
    }


class OrganizationMemberTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'contact': RelatedObjectMapping('user', SalesforceMember),
        'organization':
            RelatedObjectMapping('organization',SalesforceOrganization),
        'role': 'function'
    }


class ProjectTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'project_name': 'title',
        'describe_the_project_in_one_sentence': CropMapping('pitch', 5000),
        'video_url': 'video_url',
        'is_campaign': 'is_campaign',

        'amount_at_the_moment': EuroMapping('amount_donated'),
        'amount_requested': EuroMapping('amount_asked'),
        'amount_still_needed': EuroMapping('amount_needed'),
        'donation_total':  EuroMapping('amount_donated'),
        'donation_oo_total':  EuroMapping('amount_donated'),

        'allow_overfunding': 'allow_overfunding',
        'story': 'story',

        'picture_location': ImageMapping('image'),

        'date_project_deadline': DateTimeMapping('deadline'),
        'project_created_date': DateTimeMapping('created'),
        'project_updated_date': DateTimeMapping('updated'),
        'date_plan_submitted': DateTimeMapping('date_submitted'),
        'date_started': DateTimeMapping('campaign_started'),
        'date_ended': DateTimeMapping('campaign_ended'),
        'date_funded': DateTimeMapping('campaign_funded'),

        'country_in_which_the_project_is_located': CountryMapping('country'),
        'sub_region': SubRegionMapping('country'),
        'region': RegionMapping('country'),
        'theme': RelatedMapping('theme.name'),
        'status_project': RelatedMapping('status.name'),

        'tags': TagsMapping('tags'),
        'partner_organization': RelatedMapping('partner_organization.name'),

        'slug': 'slug',
        'supporter_count': MethodMapping('supporters_count'),
        'supporter_oo_count': MethodMapping('supporters_count', True),

        'project_owner': RelatedObjectMapping('owner', SalesforceMember),
        'organization_account':
            RelatedObjectMapping('organization', SalesforceOrganization),

    }

class FundraiserTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'owner': RelatedObjectMapping('owner', SalesforceMember),
        'project': RelatedObjectMapping('project', SalesforceProject),
        'picture_location':  ImageMapping('image'),
        'name': CropMapping('title', 80),
        'description': 'description',
        'video_url': 'video_url',
        'amount':  EuroMapping('amount'),
        'amount_at_the_moment': EuroMapping('amount_donated'),
        'deadline': DateMapping('deadline'),
        'created': DateTimeMapping('created'),
    }


class ProjectBudgetLineTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'costs':  EuroMapping('amount'),
        'description': 'description',
        'project': RelatedObjectMapping('project', SalesforceProject)
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

        'close_date': DateTimeMapping('completed'),
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
        'extended_task_description': 'description',
        'location_of_the_task': 'location',
        'people_needed': 'people_needed',
        # 'end_goal': 'end_goal',

        'task_expertise': RelatedMapping('skill.name'),

        'task_status': 'status',
        'title': 'title',
        'task_created_date': DateTimeMapping('created'),
        'tags': TagsMapping('tags'),

        # 'date_realized':
    }


class TaskMemberTransformer(BaseTransformer):

    field_mapping = {

        'external_id': 'id',
        'contacts': RelatedObjectMapping('member', SalesforceMember),
        'x1_club_task': RelatedObjectMapping('task', SalesforceTask),
        'motivation': 'motivation',
        'status': ChoiceMapping('status'),
        'taskmember_created_date': DateTimeMapping('created')
    }
