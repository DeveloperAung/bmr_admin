# Generated by Django 5.1.7 on 2025-03-25 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteInfo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='siteinfo',
            name='contact',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='siteinfo',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
