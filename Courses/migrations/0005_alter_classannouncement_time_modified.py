# Generated by Django 3.2.7 on 2021-11-30 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0004_auto_20211201_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classannouncement',
            name='time_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]