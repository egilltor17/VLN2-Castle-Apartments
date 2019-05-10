# Generated by Django 2.2.1 on 2019-05-10 10:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('realEstate', '0002_auto_20190509_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='dateCreated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='property',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]