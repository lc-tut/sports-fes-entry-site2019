from django.db import models
from django.utils.translation import gettext_lazy as _

class Member(models.Model):
    GRADE = ((1, '1年'), (2, '2年'), (3, '3年'), (4, '4年')) #settings.pyに切り出すのがいいかも

    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'), help_text=_('Use your email address (@edu.teu.ac.jp)'))
    grade = models.IntegerField(default=1, choices=GRADE)
    experience = models.BooleanField(default=False)
    team = models.ForeignKey('Team', related_name='members', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Team(models.Model):
    #settings.pyに切り出すのがいいかも
    SOCCER = "Soccer"
    BASKETBALL = "BasketBall"
    TENNIS = "Tennis"

    EVENT_CHOICES = (
        (SOCCER, SOCCER),
        (BASKETBALL, BASKETBALL),
        (TENNIS, TENNIS),
    )

    name = models.CharField(max_length=50)
    event = models.CharField(max_length=15, choices=EVENT_CHOICES, default=SOCCER)
    leader = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='leading')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name