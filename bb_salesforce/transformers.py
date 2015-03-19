from bb_salesforce.mappings import (
    CropMapping, StringMapping, CountryMapping,
    ConcatenateMapping, EmailMapping, TagsMapping,
    ChoiceMapping)
from .base import BaseTransformer


class OrganizationTransformer(BaseTransformer):

    field_mapping = {
        'external_id': 'id',
        'name': 'name',
        'billing_city': CropMapping(40, 'city'),
        'billing_street': ConcatenateMapping(['address_line1', 'address_line2']),

        'billing_postal_code': 'postal_code',
        'billing_state': CropMapping(20, 'state'),
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

        # contact.category1 = Member.UserType.values[user.user_type].title()

        'contact.category1': ChoiceMapping('user_type'),


        'first_name':  'first_name',
        'last_name': StringMapping('last_name', default="Member"),

        # contact.location = user.location
        # contact.website = user.website
        #
        # contact.picture_location = ""
        # if user.picture:
        #     contact.picture_location = str(user.picture)
        #
        # contact.about_me_us = user.about
        # contact.why_one_percent_member = user.why
        #
        # contact.availability = user.available_time
        #
        # contact.facebook = user.facebook
        # contact.twitter = user.twitter
        # contact.skype = user.skypename
        #
        # contact.primary_language = user.primary_language
        # contact.receive_newsletter = user.newsletter
        # contact.phone = user.phone_number
        # contact.birth_date = user.birthdate
        #
        # if user.gender == "male":
        #     contact.gender = Member.Gender.values['male'].title()
        # elif user.gender == "female":
        #     contact.gender = Member.Gender.values['female'].title()
        # else:
        #     contact.gender = ""
        #
        # contact.tags = ""
        # for tag in user.tags.all():
        #     contact.tags = str(tag) + ", " + contact.tags
        #
        # if user.address:
        #     contact.mailing_city = user.address.city
        #     contact.mailing_street = user.address.line1 + ' ' + user.address.line2
        #     if user.address.country:
        #         contact.mailing_country = user.address.country.name
        #     else:
        #         contact.mailing_country = ''
        #     contact.mailing_postal_code = user.address.postal_code
        #     contact.mailing_state = user.address.state
        # else:
        #     contact.mailing_city = ''
        #     contact.mailing_street = ''
        #     contact.mailing_country = ''
        #     contact.mailing_postal_code = ''
        #     contact.mailing_state = ''
        #
        # # Determine if the user has activated himself, by default assume not
        # # if this is a legacy record, by default assume it has activated
        # contact.has_activated = True
        #
        # contact.last_login = user.last_login
        #
        # # Bank details of recurring payments
        # try:
        #     monthly_donor = MonthlyDonor.objects.get(user=user)
        #     contact.bank_account_city = monthly_donor.city
        #     contact.bank_account_holder = monthly_donor.name
        #     contact.bank_account_number = ''
        #     contact.bank_account_iban = monthly_donor.iban
        #     contact.bank_account_active_recurring_debit = monthly_donor.active
        # except MonthlyDonor.DoesNotExist:
        #     contact.bank_account_city = ''
        #     contact.bank_account_holder = ''
        #     contact.bank_account_number = ''
        #     contact.bank_account_iban = ''
        #     contact.bank_account_active_recurring_debit = False

    }