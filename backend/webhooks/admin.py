from django.contrib import admin
from .models import ticket_assignment, ticket_status_changes

admin.site.register(ticket_status_changes)
admin.site.register(ticket_assignment)
