# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2022-08-03 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Libsys', '0002_auto_20220803_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='book_location',
            field=models.CharField(max_length=100),
        ),
    ]
