# Generated by Django 2.1.7 on 2019-04-27 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_member_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_registered',
            field=models.BooleanField(default=True),
        ),
    ]