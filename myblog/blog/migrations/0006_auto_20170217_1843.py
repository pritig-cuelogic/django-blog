# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 18:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_auto_20170216_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_count', models.IntegerField(default=0)),
                ('unlike_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='is_like',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='like_count',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='unlike_count',
        ),
        migrations.AddField(
            model_name='usercomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Comment'),
        ),
        migrations.AddField(
            model_name='usercomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
