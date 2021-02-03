from django.db import models

# Model for Driver Table
class DriverUser(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=30)
