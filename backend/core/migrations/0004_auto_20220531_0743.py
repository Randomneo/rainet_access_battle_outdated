# Generated by Django 3.2 on 2022-05-31 07:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20220529_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='loser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lost_boards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='board',
            name='state',
            field=models.CharField(choices=[(1, 'In Progress'), (2, 'Finished'), (10, 'Dropped')], default=1, max_length=32),
        ),
        migrations.AddField(
            model_name='board',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='won_boards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='board',
            name='player2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='boards2', to=settings.AUTH_USER_MODEL),
        ),
    ]
