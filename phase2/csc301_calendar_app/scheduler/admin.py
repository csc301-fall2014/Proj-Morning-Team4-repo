from django.contrib import admin

from scheduler.models import Calendar, Event

# Register your models here.

class CalendarAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Calendar)
admin.site.register(Event)
