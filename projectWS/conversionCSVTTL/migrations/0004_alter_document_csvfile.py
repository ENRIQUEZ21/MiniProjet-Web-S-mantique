# Generated by Django 3.2.8 on 2021-10-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversionCSVTTL', '0003_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='CSVfile',
            field=models.FileField(upload_to='CSVfiles'),
        ),
    ]
