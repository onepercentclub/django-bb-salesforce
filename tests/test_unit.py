from decimal import Decimal

from django.template import Template, Context, TemplateSyntaxError
from django.utils import unittest

from bb_salesforce.mappings import CropMapping, ConcatenateMapping, EmailMapping, \
    EuroMapping
from bb_salesforce.transformers import MemberTransformer

from tests.factories import MemberFactory
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
        self.member1 = MemberFactory.create(
            username='Vlammetje', first_name='Henk',last_name='Wijngaarden',
            email='henk@vlamindepijp.nl', budget=Decimal(15.5),
            gender='m')

    def test_member_transformer(self):
        transformer = MemberTransformer()
        value_dict = transformer.transform(self.member1)
        print value_dict

