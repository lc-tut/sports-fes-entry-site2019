# Generated by Django 2.1.7 on 2019-04-28 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20190427_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='is_registered',
            field=models.BooleanField(default=True),
        ),
    ]
