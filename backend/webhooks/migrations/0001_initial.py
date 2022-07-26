# Generated by Django 4.0.6 on 2022-07-21 15:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('check_in', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ticket_status_changes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('jira_issue_key', models.CharField(max_length=24)),
                ('old_status', models.CharField(choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Testing', 'Testing'), ('DONE', 'Done')], max_length=12)),
                ('new_status', models.CharField(choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Testing', 'Testing'), ('DONE', 'Done')], max_length=12)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ticket_assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('jira_issue_key', models.CharField(max_length=24)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='check_in.person')),
            ],
        ),
    ]
