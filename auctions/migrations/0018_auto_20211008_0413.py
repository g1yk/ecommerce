# Generated by Django 3.2.8 on 2021-10-08 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_listing_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bidder',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bidders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to=settings.AUTH_USER_MODEL),
        ),
    ]
