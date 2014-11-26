from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import *
from notifications.models import Notification
from school.models import Course, SchoolProfile
from main.models import UserProfile

created_event = Signal(providing_args=["event", "owner_type", "owner_id", "user"])
updated_event = Signal(providing_args=["event", "owner_type", "owner_id", "user"])


def send_event_notifications(notification_type, owner_type, owner_id, event, user):
    # For an event, we see who the event belongs to.
    # If personal, then notification objects created only for user
    # If course calendar, then created for instructors as well as students
    # If school then created for all students enrolled in the school

    notification = notification_type + "_" + owner_type + "_event"
    owner_id = int(owner_id)
    if owner_type == "course":
        course = Course.objects.filter(id=owner_id)
        if course :
            students = UserProfile.objects.filter(courses__id=owner_id)
            instructor = course[0].creator

            for student in students:
                Notification.objects.create(notification_type=notification,
                                    content_object = event,
                                    owner=course[0],
                                    user=student.user)

            Notification.objects.create(notification_type=notification,
                                        content_object = event,
                                        owner=course[0],
                                        user=instructor)
    elif owner_type == "school":
        school = SchoolProfile.objects.filter(id=owner_id)
        if school:
            students = UserProfile.objects.filter(school__id=owner_id)

            for student in students:
                Notification.objects.create(notification_type=notification,
                                            content_object = event,
                                            owner=school[0],
                                            user=student.user)
    else:
        Notification.objects.create(notification_type=notification,
                                content_object = event,
                                owner=user,
                                user=user)

@receiver(created_event)
def create_new_event_notification(sender, **kwargs):

    send_event_notifications(notification_type="new",
                            owner_type=kwargs.get("owner_type"),
                            owner_id=kwargs.get("owner_id"),
                            event=kwargs.get("event"),
                            user=kwargs.get("user"))


@receiver(updated_event)
def update_new_event_notification(sender, **kwargs):
    send_event_notifications(notification_type="updated",
                            owner_type=kwargs.get("owner_type"),
                            owner_id=kwargs.get("owner_id"),
                            event=kwargs.get("event"),
                            user=kwargs.get("user"))