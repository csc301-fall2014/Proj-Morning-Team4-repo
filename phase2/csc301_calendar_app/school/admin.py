from django.contrib import admin

from school.models import SchoolProfile, Course

# Register your models here.
admin.site.register(SchoolProfile)
admin.site.register(Course)
