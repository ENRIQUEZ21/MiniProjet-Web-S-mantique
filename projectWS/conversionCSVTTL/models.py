# Authors: Aurélien NICOLLE - Ilan SOUSSAN - Antoine DARRAS - Gabriel ENRIQUEZ
# Date: 26/10/2021
from django.db import models


# Create your models here.
from .validators import validate_file_extension


class Document(models.Model):
    CSVfile = models.FileField(upload_to='CSVfiles', validators=[validate_file_extension])
    delimitation = models.CharField(blank=True, max_length=1, null=True)
    if_title = models.BooleanField(default=True)
    title_row = models.IntegerField(blank=True, null=True)
    start_row = models.IntegerField()
    end_row = models.IntegerField()
