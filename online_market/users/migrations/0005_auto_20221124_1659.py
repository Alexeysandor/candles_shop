# Generated by Django 3.0 on 2022-11-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20221124_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='address',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='first_name',
            field=models.CharField(default='', max_length=50, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='phone_number',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='postal_code',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='second_name',
            field=models.CharField(default='', max_length=50, verbose_name='Фамилия'),
        ),
    ]
