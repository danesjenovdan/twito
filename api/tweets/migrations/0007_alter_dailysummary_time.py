# Generated by Django 4.0.1 on 2022-02-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0006_dailysummary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysummary',
            name='time',
            field=models.IntegerField(null=True),
        ),
    ]
