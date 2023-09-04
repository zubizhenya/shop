# Generated by Django 4.2.4 on 2023-08-19 05:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0006_alter_bb_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='title',
            field=models.CharField(error_messages={'invalid': 'Неправильное название товара'}, max_length=50, validators=[django.core.validators.RegexValidator(regex='^.1')], verbose_name='Товар'),
        ),
    ]