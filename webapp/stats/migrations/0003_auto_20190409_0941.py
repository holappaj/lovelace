# Generated by Django 2.0.2 on 2019-04-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20190408_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttaskstats',
            name='first_answer',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='studenttaskstats',
            name='first_correct',
            field=models.DateTimeField(null=True),
        ),
    ]
