from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


#from django.contrib.auth.models import UserProfile

# Create your models here.

# Create your models here.
class Calendar(models.Model):

    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

class Event(models.Model):

    name = models.CharField(blank=False, max_length=128)
    description = models.CharField(blank=True, max_length = 500)
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    location = models.CharField(blank=False, max_length=128)
    creator = models.ForeignKey(User)
    cal = models.ForeignKey(Calendar)

    def clean(self):
        if (self.start and self.end and self.start > self.end):
            raise ValidationError('Finish time should be greater than the start time')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Event, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.name
