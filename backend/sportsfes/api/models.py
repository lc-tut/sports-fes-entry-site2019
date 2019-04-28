from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.functional import lazy

class Member(models.Model):

    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'), help_text=_('Use your email address (@edu.teu.ac.jp)'))
    experience = models.BooleanField()
    team = models.ForeignKey('Team', related_name='members', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    SOCCER = "Soccer"
    BASKETBALL = "BasketBall"
    TENNIS = "Tennis"
    BADMINTON = "Badminton"
    TABLETENNIS = "TableTennis"
    VOLLEYBALL = "VolleyBall"

    EVENT_CHOICES = (
        (SOCCER, SOCCER),
        (BASKETBALL, BASKETBALL),
        (TENNIS, TENNIS),
        (BADMINTON, BADMINTON),
        (TABLETENNIS, TABLETENNIS),
        (VOLLEYBALL, VOLLEYBALL),
    )

    name = models.CharField(max_length=50)
    event = models.CharField(max_length=15, choices=EVENT_CHOICES)
    leader = models.OneToOneField('api.Member', on_delete=models.CASCADE, related_name='leading', blank=True, null=True)
    is_registered = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name   