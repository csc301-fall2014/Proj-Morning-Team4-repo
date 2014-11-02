from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    nickname = models.CharField(max_length=128, unique=True)
    
    school = models.CharField(max_length=129, default='UofT' )

    def __unicode__(self):
        return self.user.username
    
    def getSchool(self):
            return self.school   
