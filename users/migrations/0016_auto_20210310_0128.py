# Generated by Django 3.1.5 on 2021-03-10 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20210301_0230'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='sponsor',
        #     name='security_answer',
        #     field=models.CharField(default='', max_length=60),
        # ),
        migrations.AddField(
            model_name='sponsor',
            name='security_question',
            field=models.CharField(default='', max_length=60),
        ),
    ]
