# Generated by Django 4.2.4 on 2023-08-17 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0003_rubric_alter_bb_options_alter_bb_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='kind',
            field=models.CharField(choices=[('b', 'Куплю'), ('c', 'Продам'), ('e', 'Обменяю')], default='c', max_length=1),
        ),
    ]
