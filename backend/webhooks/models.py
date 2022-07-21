from django.db import models
from django.utils import timezone, dateformat
from check_in.models import Person

class ticket_assignment(models.Model):
    assigned_at = models.DateTimeField(default=timezone.now)
    assigned_to = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    jira_issue_key = models.CharField(max_length=24)

    def __str__(self):
        return self.jira_issue_key

class ticket_status_changes(models.Model):

    class Status(models.TextChoices):
        TO_DO = "To Do"
        IN_PROGRESS = "In Progress"
        TESTING = "Testing"
        DONE = "DONE"

    updated_at = models.DateTimeField(default=timezone.now)
    jira_issue_key = models.CharField(max_length=24)
    old_status = models.CharField(max_length=12, choices=Status.choices)
    new_status = models.CharField(max_length=12, choices=Status.choices)
    description = models.CharField(max_length=150) #issue title

    def __str__(self):
        return self.jira_issue_key
    
