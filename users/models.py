from django.db import models

# Model for Driver Table - this is missing some fields, will have to f=decide how to fill out later
class Driver(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=30)
	phone_num = models.CharField(max_length=15)
	email = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
