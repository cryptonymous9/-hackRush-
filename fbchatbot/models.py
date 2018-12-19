from django.db import models

class patient(models.Model):
    contact = models.IntegerField()
    name = models.CharField(max_length = 100)

class reminder(models.Model):
    user = models.ForeignKey(patient, on_delete = models.CASCADE)
    event = models.CharField(max_length = 200)
    date = models.CharField(max_length = 20)
    time = models.CharField(max_length = 20)