# Generated by Django 4.2.14 on 2024-07-14 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RelayEntry', '0002_remove_couponcode_created_by_remove_event_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='event',
        ),
    ]
