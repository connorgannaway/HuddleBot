from django.db import models
from django.utils import timezone
from check_in.models import Person
from django.utils.translation import gettext_lazy as _

'''
This file defines database tables for the Django ORM. Each class is a table, with variables being columns.
PK is automatically included.

___str___ returns the title of an instance, instead of titles being: <Object 1>
'''

class ticket_assignment(models.Model):
    assigned_at = models.DateTimeField(default=timezone.now)
    jira_issue_key = models.CharField(max_length=24)

    #sets to null if reference is deleted
    assigned_to = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.jira_issue_key

class ticket_status_changes(models.Model):

    #status choices enum
    class Status(models.TextChoices):
        TO_DO = "to_do", _("To Do")
        IN_PROGRESS = "in_progress", _("In Progress")
        TESTING = "testing", _("Testing")
        DONE = "done", _("Done")

    updated_at = models.DateTimeField(default=timezone.now)
    jira_issue_key = models.CharField(max_length=24)
    old_status = models.CharField(max_length=12, choices=Status.choices)
    new_status = models.CharField(max_length=12, choices=Status.choices)
    description = models.CharField(max_length=150) #issue title

    def __str__(self):
        return self.jira_issue_key
    
class api_token(models.Model):
    class Services(models.TextChoices):
        SLACK = "slack"
        JIRA = "jira"

    service = models.CharField(max_length=5, choices=Services.choices)
    token = models.CharField(max_length=1350)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.service} token {self.updated_at}"
