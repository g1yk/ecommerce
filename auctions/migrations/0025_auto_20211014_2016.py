# Generated by Django 3.2.6 on 2021-10-14 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_alter_listing_photo'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='listing',
            name='auctions_listing_file_or_url',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='image_url',
        ),
    ]