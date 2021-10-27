# Generated by Django 3.2.8 on 2021-10-27 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversionCSVTTL', '0007_auto_20211027_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_title', models.BooleanField(default=True)),
                ('title_row', models.IntegerField(blank=True, null=True)),
                ('start_row', models.IntegerField()),
                ('end_row', models.IntegerField()),
                ('prefix_subj', models.CharField(blank=True, default='@prefix d: <http://ex.org/data/> .\n', max_length=1)),
                ('prefix_pred', models.CharField(blank=True, default='@prefix p: <http://ex.org/pred#> .\n\n', max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='delimitation',
            field=models.CharField(blank=True, default=',', max_length=1),
        ),
    ]
