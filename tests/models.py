from django.utils import timezone
from django.db import models

from djchoices import DjangoChoices, ChoiceItem
from django_extensions.db.fields import ModificationDateTimeField


class Address(models.Model):

    line1 = models.CharField(max_length=100, blank=True)
    line2 = models.CharField(max_length=100, blank=True)



class Member(models.Model):
    class Gender(DjangoChoices):
        male = ChoiceItem('m', label='Male')
        female = ChoiceItem('f', label='Female')

    class UserType(DjangoChoices):
        normal = ChoiceItem('n', label='Normal')
        special = ChoiceItem('s', label='Special')

    class Languages(DjangoChoices):
        dutch = ChoiceItem('dutch', label='Dutch')
        other = ChoiceItem('other', label='Foreign')

    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    gender = models.CharField(max_length=6, blank=True,
                              choices=Gender.choices)
    user_type = models.CharField(max_length=6, blank=True,
                                 choices=UserType.choices)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updated = ModificationDateTimeField(default=timezone.now)
    deleted = models.DateTimeField(default=timezone.now)

    location = models.CharField(max_length=100, blank=True)
    picture = models.FileField(upload_to='profiles', blank=True)
    about_me = models.TextField(max_length=265, blank=True)

    primary_language = models.CharField(max_length=5,
                                        choices=Languages.choices)

    phone_number = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True, blank=True)


