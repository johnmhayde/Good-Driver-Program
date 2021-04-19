from django.db import models
from PIL import Image
import datetime
from django_resized import ResizedImageField


# Model for the User Table - all users will be stored in here and this table will be checked on login
class GenericUser(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	security_question = models.CharField(max_length=60, default = "")
	# security_answer = models.CharField(max_length=60, default = "")
	type = models.CharField(max_length=15)

# Model for Driver Table - this is missing some fields, will have to decide how to fill out later
class Driver(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=30)
	phone_num = models.CharField(max_length=15)
	email = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	security_question = models.CharField(max_length=60, default = "")
	# security_answer = models.CharField(max_length=60, default = "")
	points = models.IntegerField(default=0)
	point_change_temp = models.IntegerField(default=0)
	# ADDED
	sponsor = models.CharField(max_length=50, default = "")
	profile_photo = ResizedImageField(quality=50, default='default.jpg', upload_to='profile_photos')


# Changed name of admin to avoid error thrown during migration
class GenericAdmin(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)


class Sponsor(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=15, default="")
    email = models.CharField(max_length=30, default="")
    address = models.CharField(max_length=50, default="")
    sponsor_company = models.CharField(max_length=30, default="")
    security_question = models.CharField(max_length=60, default="")
    # security_answer = models.CharField(max_length=60, default="")
    list_last_search = models.CharField(max_length=50, default="candle")
    list_items_per_page = models.IntegerField(default=25)
    list_sort_order = models.CharField(max_length=4, default="up")  # up, down
    list_sort_on = models.CharField(max_length=7, default="created")  # created, price, score
    catalog_last_search = models.CharField(max_length=50, default="")
    catalog_items_per_page = models.IntegerField(default=25)
    catalog_sort_order = models.CharField(max_length=4, default="up")  # up, down
    catalog_sort_on = models.CharField(max_length=7, default="name")  # name, ...?
    driver_vicarious = models.CharField(max_length=30, default="")


class PointHist(models.Model):
    username = models.CharField(max_length=30)
    sponsor_username = models.CharField(max_length=30)
    sponsor_company = models.CharField(max_length=30, default="")
    date = models.CharField(max_length=30)
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=300)


class Product(models.Model):
    sponsor_company = models.CharField(max_length=30, default="")
    idNum = models.IntegerField(default=1)
    priceRaw = models.IntegerField(default=1)  # Assuming we ever reach the point of point scaling per driver...


class Application(models.Model):
	driver = models.CharField(max_length=30)
	sponsor_company = models.CharField(max_length=30, default="")
	date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=10)
	reason = models.CharField(max_length=300, default="")

class Sponsorship(models.Model):
	sponsor_company = models.CharField(max_length=30, default = "")
	driver = models.CharField(max_length=30)
	driver_points = models.IntegerField(default=0)
	price_scalar = models.FloatField(default=1)

class DriverOrder(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    productName = models.CharField(max_length=30,default="")
    sponsor_company = models.CharField(max_length=30,default="")
    customer = models.ForeignKey(Driver, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    orderStatus = models.CharField(max_length=30,default="")
