# Generated by Django 3.2.9 on 2021-11-20 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistic_solution', '0004_place_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='score',
            field=models.IntegerField(default=5, verbose_name='score'),
        ),
    ]
