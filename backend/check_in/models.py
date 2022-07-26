import uuid
from django.db import models
from django.utils import timezone, dateformat


'''
This file defines database tables for the Django ORM. Each class is a table, with variables being columns.
PK is automatically included.

___str___ returns the title of an instance, instead of titles being: <Object 1>
'''

class Person(models.Model):
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    slack_id = models.CharField(max_length=24, unique=True)
    jira_id = models.CharField(max_length=24, unique=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class check_in(models.Model):
    def getCurrentDate():
        return timezone.now().date()

    #fields are null when entry is created, non-null after form submission (PATCH)
    submitted_at = models.DateTimeField(blank=True, null=True)
    feeling = models.CharField(max_length=150, blank=True, null=True)
    prior_work = models.CharField(max_length=150, blank=True, null=True)
    planned_work = models.CharField(max_length=150, blank=True, null=True)
    blockers = models.CharField(max_length=150, blank=True, null=True)

    #sets to null if reference is deleted
    user = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    
    #created at inital POST
    date = models.DateField(default=getCurrentDate)
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        user = Person.objects.get(id=self.user_id)
        return f"{user.first_name} {user.last_name} - {self.date}"

class prompt_message(models.Model):
    sent_at = models.DateTimeField(default=timezone.now)
    slack_id = models.CharField(max_length=24)
    message_body = models.CharField(max_length= 200)

    #sets to null if reference is deleted
    user = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        date = dateformat.format(self.submitted_at, 'Y-m-d H:i:s')
        user = Person.objects.get(id=self.user_id)
        return f"{user.first_name} {user.last_name} - {date}"
