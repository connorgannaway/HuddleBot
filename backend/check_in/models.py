from django.db import models
from django.utils import timezone, dateformat

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    slack_id = models.CharField(max_length=24)
    jira_id = models.CharField(max_length=24)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class check_in(models.Model):
    user_id = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    feeling = models.CharField(max_length=150)
    prior_work = models.CharField(max_length=150)
    planned_work = models.CharField(max_length=150)
    blockers = models.CharField(max_length=150)

    def __str__(self):
        date = dateformat.format(self.submitted_at, 'Y-m-d')
        user = Person.objects.first(id=self.user_id)
        return f"{user.first_name} {user.last_name} - {date}"

class prompt_message(models.Model):
    user_id = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    sent_at = models.DateTimeField(default=timezone.now)
    slack_id = models.CharField(max_length=24)
    message_body = models.CharField(max_length= 200)

    def __str__(self):
        date = dateformat.format(self.submitted_at, 'Y-m-d H:i:s')
        user = Person.objects.first(id=self.user_id)
        return f"{user.first_name} {user.last_name} - {date}"
