from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import *
from notifications.models import Notification
from school.models import Course
from main.models import UserProfile

created_event = Signal(providing_args=["owner_type", "owner_id", "user"])

@receiver(created_event)
def create_new_event_notification(sender, **kwargs):

    # For an event, we see who the event belongs to.
    # If personal, then notification objects created only for user
    # If course calendar, then created for instructors as well as students
    # If school then created for all students enrolled in the school
    if (kwargs.get('owner_type') == "user"):
        Notification.objects.create(user=kwargs.get('user'),
                                title="Event added",
                                message="An event has been added to your personal calendar")

    elif (kwargs.get('owner_type') == "course"):
        course = Course.objects.filter(id=int(kwargs.get('owner_id')))
        if course :
            students = UserProfile.objects.filter(courses__id=int(course[0].id))
            instructor = course[0].creator

            for student in students:
                Notification.objects.create(user=student.user,
                                    title="Course event added",
                                    message="An event has been added to the course " + course[0].code)

            Notification.objects.create(user=instructor,
                                    title="Course event added",
                                    message="An event has been added to the course  " + course[0].code)

#created_event.disconnect(create_new_event_notification)
