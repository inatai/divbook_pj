from django.contrib import admin
from .models import Item, Schedule, Event, Participant

# Register your models here.

admin.site.register(Item)
admin.site.register(Schedule)
admin.site.register(Event)
admin.site.register(Participant)