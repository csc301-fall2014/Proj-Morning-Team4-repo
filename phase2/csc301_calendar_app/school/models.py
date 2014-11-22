from django.db import models
from django.contrib.auth.models import User
from scheduler.models import Calendar


# Create your models here.
class SchoolProfile(models.Model):

    name = models.CharField(max_length=128, unique=True)
    email_domain = models.CharField(max_length=128, unique=True)
    cal = models.ForeignKey(Calendar)
    admin = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def validate_user_email(self, user_email):
        return user_email.strip().lower().endswith(self.email_domain.strip().lower())

class Course(models.Model):

    code = models.CharField(max_length=10, null=False, blank=False)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500,blank=True)
    cal = models.ForeignKey(Calendar)
    school = models.ForeignKey(SchoolProfile)
    creator = models.ForeignKey(User)
    #note student admin is optional
    student_admins = models.ManyToManyField('main.Student', null=False, blank=True)

    def __unicode__(self):
        return self.name
