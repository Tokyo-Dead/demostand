# models.py
from django.db import models

class ClientEnrollment(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    enrollment_time = models.DateTimeField()  # Or TimeField if you don't need the date

