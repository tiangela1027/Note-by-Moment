# Generated by Django 3.0.7 on 2020-07-03 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0016_auto_20200703_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(verbose_name='birth day'),
        ),
    ]
