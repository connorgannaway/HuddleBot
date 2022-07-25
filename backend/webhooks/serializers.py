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
        
class api_token_serializer(serializers.ModelSerializer):
    class Meta:
        model = api_token
        fields = [
            'pk',
            'token_type',
            'token',
            'refresh_token',
            'updated_at',
        ]
        extra_kwargs = {
            "refresh_token": {"required": False}
        }
