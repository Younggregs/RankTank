# Generated by Django 2.1.7 on 2019-12-09 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rank', '0002_auto_20191209_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='firstname',
            field=models.CharField(default='Oo', max_length=20),
        ),
        migrations.AddField(
            model_name='account',
            name='lastname',
            field=models.CharField(default='Oo', max_length=20),
        ),
    ]
