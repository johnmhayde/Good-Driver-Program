# Generated by Django 3.1.5 on 2021-02-08 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210204_0228'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=15)),
            ],
        ),
    ]
