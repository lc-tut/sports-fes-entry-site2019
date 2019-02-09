from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    def create_user(self, number, username, email, grade, experience, team=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            number=number,
            username=username,
            email=self.normalize_email(email),
            grade=grade,
            experience=experience,
            team=team,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, number, username, email, grade, experience, password, team=None):
        user = self.create_user(
            number=number,
            username=username,
            email=email,
            grade=grade,
            experience=experience,
            team=team,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    GRADE = ((1, '1年'), (2, '2年'), (3,'3年'), (4, '4年'))


    number = models.CharField(max_length=150, unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_(
            'Required. 150 characters or fewer.'
        ),
        validators=[username_validator],
        unique=False
    )
    email = models.EmailField(_('email address'), blank=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=40)
    last_name = models.CharField(_('last name'), max_length=40)
    grade = models.IntegerField(default=1, choices=GRADE)
    experience = models.BooleanField(default=False)
    team = models.ForeignKey('Team', related_name='members', on_delete=models.CASCADE, null=True, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'number', 'grade', 'experience']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()


class Team(models.Model):
    TENNIS = "TENNIS"
    SOCCER = "SOCCER"
    DODGE = "DODGE"
    BASKET = "BASKET"
    VOLLEY = "VOLLEY"

    EVENT_CHOICES = (
        (TENNIS, "Tennis"),
        (SOCCER, "Soccer"),
        (DODGE, "DodgeBall"),
        (BASKET, "BasketBall"),
        (VOLLEY, "VolleyBall"),
    )

    name = models.CharField(max_length=50, unique=True)
    event = models.CharField(max_length=20, choices=EVENT_CHOICES, default=TENNIS)
    leader = models.OneToOneField(User, on_delete=models.CASCADE, related_name='t')
    
    def __str__(self):
        return self.name