# Generated by Django 2.1.7 on 2019-04-27 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_team_is_registered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='is_registered',
            field=models.BooleanField(default=False),
        ),
    ]
