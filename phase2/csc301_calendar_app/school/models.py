from django.db import models
from django.contrib.auth.models import User
from scheduler.models import Calendar

# Create your models here.
class SchoolProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.

    name = models.CharField(max_length=128, unique=True)
    email_domain = models.CharField(max_length=128, unique=True)
    cal = models.ForeignKey(Calendar)
    admin = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def validate_user_email(self, user_email):
        return user_email.endswith(self.email_domain)

class Course(models.Model):
    # This line is required. Links UserProfile to a User model instance.

    name = models.CharField(max_length=128, unique=True)
    school_id = models.ForeignKey('SchoolProfile')
    def __unicode__(self):
        return self.SchoolProfile.name
