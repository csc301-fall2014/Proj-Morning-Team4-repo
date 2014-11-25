from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import *
from notifications.models import Notification

created_event = Signal(providing_args=["owner_type", "owner_id", "user"])

@receiver(created_event)
def create_new_event_notification(sender, **kwargs):

    if (kwargs.get('owner_type') == "user"):
        # For an event, we see who the event belongs to.
        # If personal, then notification objects created only for user
        # If course calendar, then created for instructors as well as students
        # If school then created for all students enrolled in the school
        Notification.objects.create(user=kwargs.get('user'),
                                title="Event added",
                                message="An event has been added to your personal calendar")
    elif (kwargs.get('owner_type') == "course"):
        course = Course.objects.get(id=owner_id)
        students = course.UserProfile_set.all()
        instructor = course.creator

        for student in students:
            Notification.objects.create(user=kwargs.get('user').user,
                                    title="Course event added",
                                    message="An event has been added to the course " + course.code)

        Notification.objects.create(user=instructor.user,
                                    title="Course event added",
                                    message="An event has been added to the course " + course.code)
