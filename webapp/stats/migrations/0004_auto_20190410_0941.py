# Generated by Django 2.0.2 on 2019-04-10 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_contentpage_evaluation_group'),
        ('stats', '0003_auto_20190409_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.PositiveIntegerField(blank=True, null=True)),
                ('total_answers', models.PositiveIntegerField()),
                ('total_tries', models.PositiveIntegerField()),
                ('total_users', models.PositiveIntegerField()),
                ('correct_by_total', models.PositiveIntegerField()),
                ('correct_by_before_dl', models.PositiveIntegerField()),
                ('correct_by_after_dl', models.PositiveIntegerField()),
                ('tries_avg', models.FloatField()),
                ('tries_median', models.PositiveIntegerField()),
                ('time_avg', models.DurationField()),
                ('time_median', models.DurationField()),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseInstance')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.ContentPage')),
            ],
        ),
        migrations.AddField(
            model_name='studenttaskstats',
            name='last_answer',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='studenttaskstats',
            name='tries_until_correct',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
