# Generated by Django 5.1.7 on 2025-04-26 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_zip_vet_zip_code_remove_details_clinic_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='clinic_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
