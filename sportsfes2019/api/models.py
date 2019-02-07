from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Member(models.Model):
    GRADE = ((1, '1年'), (2, '2年'), (3,'3年'), (4, '4年'))

    number = models.CharField(max_length=50, default="", blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.IntegerField(default=1, choices=GRADE)
    experience = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username