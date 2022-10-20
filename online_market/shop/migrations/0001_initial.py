# Generated by Django 3.0 on 2022-10-20 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image_for_example/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название товара')),
                ('slug', models.SlugField(max_length=100, verbose_name='url товара')),
                ('description', models.TextField(verbose_name='Описание товара')),
                ('image', models.ImageField(blank=True, upload_to='products/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена товара')),
                ('available', models.BooleanField(default=True, verbose_name='Наличие товара')),
            ],
            options={
                'ordering': ('price',),
                'index_together': {('id', 'slug')},
            },
        ),
    ]
