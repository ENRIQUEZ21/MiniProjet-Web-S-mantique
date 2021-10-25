from django.db import models


# Create your models here.

class Document(models.Model):
    CSVfile = models.FileField(upload_to='CSVfiles')
    delimitation = models.CharField(max_length=1)
    if_title = models.BooleanField()
    title_row = models.IntegerField()
    start_row = models.IntegerField()
    end_row = models.IntegerField()
