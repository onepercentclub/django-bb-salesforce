import factory
from tests.models import Member, Country, SubRegion, Region, Address


class MemberFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Member

    username = factory.Sequence(lambda n: u'jd_{0}'.format(n))
    first_name = factory.Sequence(lambda f: u'John_{0}'.format(f))
    last_name = factory.Sequence(lambda l: u'Doe_{0}'.format(l))
    email = factory.Sequence(lambda l: u'user_{0}@gmail.com'.format(l))


class RegionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Region
    name = factory.Sequence(lambda n: u'Region{0}'.format(n))


class SubRegionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SubRegion
    name = factory.Sequence(lambda n: u'SubRegion{0}'.format(n))
    region = factory.SubFactory(RegionFactory)


class CountryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Country
    name = factory.Sequence(lambda n: u'Country_{0}'.format(n))
    subregion = factory.SubFactory(SubRegionFactory)


class AddressFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Address

    user = factory.SubFactory(MemberFactory)
    line1 = factory.Sequence(lambda n: u'street_{0}'.format(n))
    line2 = factory.Sequence(lambda n: u'extra_{0}'.format(n))
    city = factory.Sequence(lambda n: u'city_{0}'.format(n))
    state = factory.Sequence(lambda n: u'state_{0}'.format(n))
    postal_code = factory.Sequence(lambda n: u'zipcode_{0}'.format(n))
    country = factory.SubFactory(CountryFactory)
