import factory
from tests.models import Member


class MemberFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Member

    username = factory.Sequence(lambda n: u'jd_{0}'.format(n))
    first_name = factory.Sequence(lambda f: u'John_{0}'.format(f))
    last_name = factory.Sequence(lambda l: u'Doe_{0}'.format(l))
    email = factory.Sequence(lambda l: u'user_{0}@gmail.com'.format(l))

