from rest_framework import serializers
from .models import *

'''
Serializers lay between models and views when dealing with converting and validating json data.
'fields' variable defines which fields to serialize.
'''

class Person_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'pk',
            'first_name',
            'last_name',
            'slack_id',
            'jira_id',
            'is_active',
            'start_date',
            'end_date',
        ]
        extra_kwargs = {
            "end_date": {"required": False}
        }

class check_in_serializer(serializers.ModelSerializer):
    class Meta:
        model = check_in
        fields = [
            'pk',
            'submitted_at',
            'feeling',
            'prior_work',
            'planned_work',
            'blockers',
            'user_id',
            'date',
            'uuid'
        ]
        extra_kwargs = {
            "submitted_at": {"required": False},
            "feeling": {"required": False},
            "prior_work": {"required": False},
            "planned_work": {"required": False},
            "blockers": {"required": False},
            "user_id": {"required": False},
        }
