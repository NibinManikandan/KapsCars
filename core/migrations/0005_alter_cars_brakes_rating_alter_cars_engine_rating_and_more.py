# Generated by Django 4.2.6 on 2024-08-19 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_cars_model_remove_happinessclub_owner_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='brakes_rating',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cars',
            name='engine_rating',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cars',
            name='interior_rating',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cars',
            name='suspension_rating',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cars',
            name='transmission_rating',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cars',
            name='wheels_tyres_rating',
            field=models.IntegerField(),
        ),
    ]
