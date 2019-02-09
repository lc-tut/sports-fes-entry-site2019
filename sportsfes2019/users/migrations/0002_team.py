# Generated by Django 2.1.5 on 2019-02-07 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('event', models.CharField(choices=[('TENNIS', 'Tennis'), ('SOCCER', 'Soccer'), ('DODGE', 'DodgeBall'), ('BASKET', 'BasketBall'), ('VOLLEY', 'VolleyBall')], default='TENNIS', max_length=20)),
                ('leader', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]