# Generated by Django 4.2.4 on 2023-08-19 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0010_alter_bb_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='rubric',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='bboard.rubric', verbose_name='Рубрика'),
        ),
    ]
