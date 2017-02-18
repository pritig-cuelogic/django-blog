# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_viewers'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='unlike_count',
            field=models.IntegerField(default=0),
        ),
    ]
