from django.db import models

# Create your models here.

class PatientDetails(models.Model):
    PAT_NAME=models.CharField(max_length=1000)
    PAT_EMAIL=models.CharField(max_length=1000)

 