from django.contrib import admin
from .models import Person, check_in, prompt_message

admin.site.register(Person)
admin.site.register(check_in)
admin.site.register(prompt_message)
