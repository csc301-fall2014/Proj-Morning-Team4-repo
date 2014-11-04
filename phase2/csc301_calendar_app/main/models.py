from django.db import models
from django.contrib.auth.models import User
from scheduler.models import Calendar

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    nickname = models.CharField(max_length=128, unique=True)
    cal = models.ForeignKey(Calendar)
    school = models.CharField(max_length=129, default='UofT' )

    def __unicode__(self):
        return self.user.username
    
    def getSchool(self):
        return self.school

    class Meta:
        permissions = (
            ('create_event', 'Create an event'),
            ('join_event', 'Join an event'),
            ('leave_event', 'Leave and event'),
            ('enroll_course', 'Enroll in a course'),
            ('drop_course', 'Drop a course'),
        )
