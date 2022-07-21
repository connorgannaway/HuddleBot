from rest_framework import serializers
from .models import *

'''
Serializers lay between models and views when dealing with converting and validating json data.
'fields' variable defines which fields to serialize.
'''

class ticket_assignment_serializer(serializers.ModelSerializer):
    class Meta:
        model = ticket_assignment
        fields = [
            'pk',
            'assigned_at',
            'assigned_to',
            'jira_issue_key',
        ]
        extra_kwargs = {
            "assigned_to": {"required": False}
        }

class ticket_status_changes_serializer(serializers.ModelSerializer):
    class Meta:
        model = ticket_status_changes
        fields = [
            'pk',
            'updated_at',
            'jira_issue_key',
            'old_status',
            'new_status',
            'description',
        ]
        