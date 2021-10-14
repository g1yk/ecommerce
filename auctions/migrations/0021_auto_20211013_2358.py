# Generated by Django 3.2.6 on 2021-10-13 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20211013_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='listing',
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ManyToManyField(related_name='comments', to='auctions.Listing'),
        ),
    ]