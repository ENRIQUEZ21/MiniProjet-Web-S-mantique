# Generated by Django 3.2.8 on 2021-10-27 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversionCSVTTL', '0006_alter_document_delimitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='delimitation',
        ),
        migrations.RemoveField(
            model_name='document',
            name='end_row',
        ),
        migrations.RemoveField(
            model_name='document',
            name='if_title',
        ),
        migrations.RemoveField(
            model_name='document',
            name='start_row',
        ),
        migrations.RemoveField(
            model_name='document',
            name='title_row',
        ),
    ]
