# Authors: Aurélien NICOLLE - Ilan SOUSSAN - Antoine DARRAS - Gabriel ENRIQUEZ
# Date: 26/10/2021

from django.db import models

# Create your models here.
from .validators import validate_file_extension
from django.conf import settings

import configparser



class Document(models.Model):
    config = configparser.ConfigParser()
    config.read('.ini')
    CSVfile = models.FileField(upload_to='CSVfiles', validators=[validate_file_extension])
    delimitation = models.CharField(blank=True, max_length=1, default=config['DEFAULT']['DEFAULT_DELIMITER'])


class Information(models.Model):
    config = configparser.ConfigParser()
    config.read('.ini')
    if_title = models.BooleanField(default=True)
    title_row = models.IntegerField(blank=True, null=True)
    start_row = models.IntegerField()
    end_row = models.IntegerField()
    prefix_obj = models.CharField(max_length=25, default=config['DEFAULT']['OBJECT_PREFIX'])
    prefix_pred = models.CharField(max_length=25, default=config['DEFAULT']['PREDICATE_PREFIX'])
    file_name = models.CharField(max_length=25, default='')
    path_to_csv = models.CharField(max_length=255, default='')
    delimiter = models.CharField(blank=True, max_length=1, default=config['DEFAULT']['DEFAULT_DELIMITER'])
