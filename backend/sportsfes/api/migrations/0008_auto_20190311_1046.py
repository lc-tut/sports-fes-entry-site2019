# Generated by Django 2.1.7 on 2019-03-11 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20190307_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='experience',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='member',
            name='grade',
            field=models.IntegerField(choices=[(1, '1年'), (2, '2年'), (3, '3年'), (4, '4年')]),
        ),
    ]
