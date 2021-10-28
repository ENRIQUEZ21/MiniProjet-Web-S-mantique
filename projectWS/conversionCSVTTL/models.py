# Authors: Aurélien NICOLLE - Ilan SOUSSAN - Antoine DARRAS - Gabriel ENRIQUEZ
# Date: 28/10/2021

from django.db import models

from .validators import validate_file_extension

import configparser



class Document(models.Model):
    config = configparser.ConfigParser()
    config.read('.ini') # We read the .ini file to have the default value of the delimiter
    # File input in our form, we will upload it in the media/CSVfiles folder in our project
    CSVfile = models.FileField(upload_to='CSVfiles', validators=[validate_file_extension])
    # input for our delimiter with default value from .ini file
    delimitation = models.CharField(blank=True, max_length=1, default=config['DEFAULT']['DEFAULT_DELIMITER'])


class Information(models.Model):
    config = configparser.ConfigParser()
    config.read('.ini') # We read the .ini file to have the default value of the delimiter, the object and predicate prefixes
    if_title = models.BooleanField(default=True) # Input of our if_title field (boolean yes/no)
    title_row = models.IntegerField(blank=True, null=True) # Input of title row (possibly null)
    start_row = models.IntegerField() # Input of start row
    end_row = models.IntegerField() # Input of end row
    prefix_obj = models.CharField(max_length=25, default=config['DEFAULT']['OBJECT_PREFIX']) # input for our object prefix with default value from .ini file
    prefix_pred = models.CharField(max_length=25, default=config['DEFAULT']['PREDICATE_PREFIX']) # input for our predicate prefix with default value from .ini file
    file_name = models.CharField(max_length=25, default='') # input for the name of our TTL file
    path_to_csv = models.CharField(max_length=255, default='') # Input hidden for the path_to_csv that we will use to validate our form
    delimiter = models.CharField(blank=True, max_length=1, default=config['DEFAULT']['DEFAULT_DELIMITER']) # Input hidden for the delimiter that we will use only to validate our form
