# Generated by Django 3.1.5 on 2021-04-19 04:28

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver', models.CharField(max_length=30)),
                ('sponsor_company', models.CharField(default='', max_length=30)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(max_length=10)),
                ('reason', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('phone_num', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('security_question', models.CharField(default='', max_length=60)),
                ('points', models.IntegerField(default=0)),
                ('point_change_temp', models.IntegerField(default=0)),
                ('sponsor', models.CharField(default='', max_length=50)),
                ('profile_photo', django_resized.forms.ResizedImageField(crop=None, default='default.jpg', force_format=None, keep_meta=True, quality=50, size=[1920, 1080], upload_to='profile_photos')),
            ],
        ),
        migrations.CreateModel(
            name='GenericAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GenericUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('security_question', models.CharField(default='', max_length=60)),
                ('type', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='PointHist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('sponsor_username', models.CharField(max_length=30)),
                ('sponsor_company', models.CharField(default='', max_length=30)),
                ('date', models.CharField(max_length=30)),
                ('points', models.IntegerField(default=0)),
                ('reason', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_company', models.CharField(default='', max_length=30)),
                ('idNum', models.IntegerField(default=1)),
                ('priceRaw', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('phone_num', models.CharField(default='', max_length=15)),
                ('email', models.CharField(default='', max_length=30)),
                ('address', models.CharField(default='', max_length=50)),
                ('sponsor_company', models.CharField(default='', max_length=30)),
                ('security_question', models.CharField(default='', max_length=60)),
                ('list_last_search', models.CharField(default='candle', max_length=50)),
                ('list_items_per_page', models.IntegerField(default=25)),
                ('list_sort_order', models.CharField(default='up', max_length=4)),
                ('list_sort_on', models.CharField(default='created', max_length=7)),
                ('catalog_last_search', models.CharField(default='', max_length=50)),
                ('catalog_items_per_page', models.IntegerField(default=25)),
                ('catalog_sort_order', models.CharField(default='up', max_length=4)),
                ('catalog_sort_on', models.CharField(default='name', max_length=7)),
                ('driver_vicarious', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_company', models.CharField(default='', max_length=30)),
                ('driver', models.CharField(max_length=30)),
                ('driver_points', models.IntegerField(default=0)),
                ('price_scalar', models.FloatField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='DriverOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(default='', max_length=30)),
                ('sponsor_company', models.CharField(default='', max_length=30)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.BooleanField(default=False)),
                ('orderStatus', models.CharField(default='', max_length=30)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.driver')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.product')),
            ],
        ),
    ]
