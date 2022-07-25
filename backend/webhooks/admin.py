from django.contrib import admin
from .models import ticket_assignment, ticket_status_changes, api_token

admin.site.register(ticket_status_changes)
admin.site.register(ticket_assignment)
admin.site.register(api_token)