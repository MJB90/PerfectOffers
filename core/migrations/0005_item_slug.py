# Generated by Django 3.0.7 on 2020-06-26 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='item'),
            preserve_default=False,
        ),
    ]
