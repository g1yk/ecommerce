# Generated by Django 3.2.6 on 2021-09-30 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ManyToManyField(blank=True, default=None, to='auctions.Category'),
        ),
    ]