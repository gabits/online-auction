# Generated by Django 3.0.5 on 2020-04-19 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='highest_for_lot',
        ),
    ]