# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-09 08:43
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DengueBite',
            fields=[
                ('bite_uuid', models.TextField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lng', models.FloatField()),
                ('lat', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(default='POINT(0.0 0.0)', geography=True, srid=4326)),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
    ]
