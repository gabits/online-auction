# Generated by Django 3.0.5 on 2020-04-19 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_remove_bid_highest_for_lot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='is_active',
        ),
    ]
