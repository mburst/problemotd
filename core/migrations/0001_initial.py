# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
from django.conf import settings
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('path', djorm_pgarray.fields.ArrayField(blank=True, null=True, default=None)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('website', models.URLField(blank=True)),
                ('spam', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('text', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateField(unique=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ProblemSuggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('text', models.TextField()),
                ('problem', models.ForeignKey(null=True, to='core.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('status', models.CharField(max_length=36, blank=True, default=uuid.uuid4)),
                ('weekly', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='problem',
            field=models.ForeignKey(to='core.Problem'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
