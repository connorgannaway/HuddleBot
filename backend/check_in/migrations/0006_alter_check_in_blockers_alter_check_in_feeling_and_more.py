# Generated by Django 4.0.6 on 2022-08-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_in', '0005_alter_check_in_submitted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_in',
            name='blockers',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='check_in',
            name='feeling',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='check_in',
            name='planned_work',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='check_in',
            name='prior_work',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]