# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-09 11:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sugangpage', '0002_auto_20171209_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suganglist',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 9, 20, 32, 48, 231273)),
        ),
        migrations.AlterField(
            model_name='suganglist',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 9, 20, 32, 48, 231292)),
        ),
    ]
