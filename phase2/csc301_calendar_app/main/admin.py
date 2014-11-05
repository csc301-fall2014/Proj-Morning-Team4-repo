from django.contrib import admin

from main.models import Student, Instructor, UserProfile

# Register your models here.
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(UserProfile)
