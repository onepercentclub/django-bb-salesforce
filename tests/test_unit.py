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
        mapped = mapping(self.member1, 'nickname')
        self.assertEqual(mapped, {'nickname': 'Vlam'})

    def test_concat_mapping(self):
        mapping = ConcatenateMapping(['last_name', 'first_name'],
                                      concatenate_str=', ')
        mapped = mapping(self.member1, 'name')
        self.assertEqual(mapped, {'name': 'Wijngaarden, Henk'})

    def test_email_mapping(self):
        # Check that valid email address gets parsed
        mapping = EmailMapping('email')
        mapped = mapping(self.member1, 'email')
        self.assertEqual(mapped, {'email': 'henk@vlamindepijp.nl'})
        # Now try a user with no valid email address
        mapping = EmailMapping('email')
        mapped = mapping(self.member2, 'email')
        self.assertEqual(mapped, {'email': ''})

    def test_euro_mapping(self):
        mapping = EuroMapping('budget')
        mapped = mapping(self.member1, 'budget')
        self.assertEqual(mapped, {'budget': '15.50'})

        mapping = EuroMapping('budget')
        mapped = mapping(self.member2, 'budget')
        self.assertEqual(mapped, {'budget': '0.00'})


class TransformerTestCase(unittest.TestCase):

    def setUp(self):
        self.time1 = timezone.datetime(2015, 1, 1)

        self.member1 = MemberFactory.create(
            username='Vlammetje', first_name='Henk',last_name='Wijngaarden',
            email='henk@vlamindepijp.nl', budget=Decimal(15.5),
            gender='m',
            member_since=self.time1,
            last_login=self.time1,
            date_joined=self.time1,
            deleted=None
            )

        self.address = AddressFactory(
            user=self.member1,
            line1='Paleis',
            line2='Dam 1',
            postal_code='1000AA',
            state='',
            city='Nul Tien',
            country=CountryFactory(name='Netherlands')
            )

    def test_member_transformer(self):
        transformer = MemberTransformer()
        value_dict = transformer.transform(self.member1)

        data = {'last_name': 'Wijngaarden',
                'about_me_us': u'',
                'external_id': 9,
                'deleted': None,
                'member_since': self.time1,
                'is_active': False,
                'bank_account_city': '',
                'phone': u'',
                'mailing_postal_code': '1000AA',
                'primary_language': u'',
                'has_activated': False,
                'mailing_city': 'Nul Tien',
                'date_joined': self.time1,
                'first_name': 'Henk',
                'receive_newsletter': True,
                'mailing_state': '',
                'gender': u'Male',
                'bank_account_holder': '',
                'mailing_street': u'Paleis Dam 1',
                'contact.category1': u'',
                'mailing_country': 'Netherlands',
                'picture_location': '',
                'bank_account_iban': '',
                'bank_account_active_recurring_debit': '',
                'last_login': self.time1,
                'location': u'',
                'birth_date': None,
                'user_name': 'Vlammetje',
                'email': 'henk@vlamindepijp.nl'}

        self.assertEqual(data, value_dict)


