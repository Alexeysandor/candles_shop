# Generated by Django 3.0 on 2022-11-24 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20221124_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Имя'),
        ),
    ]