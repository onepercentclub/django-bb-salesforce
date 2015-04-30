from decimal import Decimal

from django.template import Template, Context, TemplateSyntaxError
from django.utils import unittest, timezone

from bb_salesforce.mappings import (CropMapping, ConcatenateMapping,
                                    EmailMapping,EuroMapping)
from bb_salesforce.transformers import MemberTransformer

from tests.factories import MemberFactory, AddressFactory, CountryFactory
from tests.models import Member


class MappingsTestCase(unittest.TestCase):

    def setUp(self):
        self.member1 = MemberFactory.create(
            username='Vlammetje', first_name='Henk',last_name='Wijngaarden',
            email='henk@vlamindepijp.nl', budget=Decimal(15.5),
            gender='m')

        self.member2 = MemberFactory.create(
            username='H\x543nk', first_name='Hank',last_name=None,
            email='henk#vlamindepijp.nl')

    def test_crop_mapping(self):
        mapping = CropMapping('username', 4)
        mapped = mapping(self.member1).to_field()
        self.assertEqual(mapped, 'Vlam')

    def test_concat_mapping(self):
        mapping = ConcatenateMapping(['last_name', 'first_name'],
                                      concatenate_str=', ')
        mapped = mapping(self.member1).to_field()
        self.assertEqual(mapped, 'Wijngaarden, Henk')

    def test_email_mapping(self):
        # Check that valid email address gets parsed
        mapping = EmailMapping('email')
        mapped = mapping(self.member1).to_field()
        self.assertEqual(mapped, 'henk@vlamindepijp.nl')
        # Now try a user with no valid email address
        mapping = EmailMapping('email')
        mapped = mapping(self.member2).to_field()
        self.assertEqual(mapped, '')

    def test_euro_mapping(self):
        mapping = EuroMapping('budget')
        mapped = mapping(self.member1).to_field()
        self.assertEqual(mapped, '15.50')

        mapping = EuroMapping('budget')
        mapped = mapping(self.member2).to_field()
        self.assertEqual(mapped, '0.00')


class TransformerTestCase(unittest.TestCase):

    def setUp(self):
        self.time = timezone.datetime(2015, 1, 1)
        self.time_flat = '2015-01-01T00:00:00.000Z'

        self.member1 = MemberFactory.create(
            username='Vlammetje', first_name='Henk',last_name='Wijngaarden',
            email='henk@vlamindepijp.nl', budget=Decimal(15.5),
            gender='m',
            member_since=self.time,
            last_login=self.time,
            date_joined=self.time,
            deleted=None
            )

        self.address = AddressFactory(
            user=self.member1,
            line1='Paleis',
            line2='Dam 1',
            postal_code='1000AA',
            state='',
            city='Nul Twintig',
            country=CountryFactory(name='Netherlands')
            )

        self.maxDiff = None



    def test_member_transformer(self):
        transformer = MemberTransformer(self.member1)
        value_dict = transformer.to_dict()

        data = {'MailingPostalCode': '1000AA',
                'Member_since__c': self.time,
                'MailingStreet': u'Paleis Dam 1',
                'Has_Activated_Account__c': False,
                'FirstName': 'Henk',
                'LastName': 'Wijngaarden',
                'Account_IBAN__c': '',
                'Account_Active_Recurring_Debit__c': '',
                'Birthdate': None,
                'Date_Joined__c': self.time,
                'Deleted__c': None,
                'Primary_language__c': u'',
                'Username__c': 'Vlammetje',
                'Date_Last_Login__c': self.time,
                'MailingState': '',
                'Email': 'henk@vlamindepijp.nl',
                'Receive_newsletter__c': True,
                'Account_holder__c': '',
                'Gender__c': u'Male',
                'Picture_Location__c': '',
                'Location__c': u'',
                'Phone': u'',
                'Facebook__c': None,
                'MailingCity': 'Nul Twintig',
                'Category1__c': u'',
                'MailingCountry': 'Netherlands',
                'Account_city__c': '',
                'Active__c': False,
                'external_id': 9,
                'Website__c': None}

        # Try transform to_field
        self.assertEqual(data, value_dict)

        value_list = transformer.to_csv()

        print value_list

        data = ['1000AA',
                'Vlammetje',
                'Henk',
                'Wijngaarden',
                '',
                '',
                '',
                '',
                'henk@vlamindepijp.nl',
                '0',
                '1',
                'Male',
                '',
                'Nul Twintig',
                '',
                '',
                '2015-01-01T00:00:00.000Z',
                'Paleis Dam 1',
                None,
                'Netherlands',
                '',
                '',
                '2015-01-01T00:00:00.000Z',
                '',
                '2015-01-01T00:00:00.000Z',
                '',
                None,
                '',
                '0',
                '9']



        # Try transform to_csv
        self.assertEqual(data, value_list)
