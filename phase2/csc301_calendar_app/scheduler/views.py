from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main.models import Student
from scheduler.models import Calendar, Event
from scheduler.forms import EventForm
import json


def verified_calendar(owner_type, owner_id, user):
    """Return a calendar owned by owner_id only if the current user has
    permission to view the calendar
    If the owner_type is a school or a course, ensure that the user is
    enrolled"""

    if (owner_type == 'user'):
        if (user.id == int(owner_id)):
            calendar = Student.objects.get(user=user).cal
        else:
            return HttpResponse('PERMISSION DEINED! GTFO')
    elif (owner_type == 'school'):
        # make sure the user belongs to the school with owner_id
        # return the school calendar
        calendar = ""
    elif (owner_type == 'course'):
        # make sure the user is enrolled in the course with owner_id
        # return teh course calendar
        calendar = ""

    return calendar

@login_required
def calendar_view_basic(request, owner_type, owner_id):
    """Return a calendar owned by owner_id only if the current user has
    permission to view the calendar"""

    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    user = request.user

    if request.method == 'GET':
        verified_obj = verified_calendar(owner_type, owner_id, user)
        if isinstance(verified_obj, Calendar):
            calendar = verified_obj
            events = calendar.event_set.all()
        else:
            return verified_obj

        return render_to_response('scheduler/calendar_basic.html',
                    {'calendar' : calendar, 'events': events}, context)
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('main/login.html', {}, context)

@login_required
def add_event(request, owner_type, owner_id):
    """ Add an event to the calendar belonging to the owner of ownder id only
    if the current user has permission to do so"""

     # Like before, get the request's context.
    context = RequestContext(request)
    event_added = False

    user = request.user
     # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        verified_obj = verified_calendar(owner_type, owner_id, user)
        if isinstance(verified_obj, Calendar):
            calendar = verified_obj
        else:
            return verified_obj

        # Attempt to grab information from the raw form information.
        event_form = EventForm(data=request.POST)
        if event_form.is_valid():
            # Save the event's form data to the database.
            event = event_form.save(commit=False)
            event.cal = calendar
            event.creator = user

            event.save()

            event_added = True
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print event_form.errors

    # Not a HTTP POST, so we render our form using the EventForm.
    # These forms will be blank, ready for user input.
    else:
        event_form = EventForm()

    # Render the template depending on the context.
    return render_to_response(
            'scheduler/add_event.html', {'event_form': event_form, 'user' : user,
            'event_added': event_added},
            context)

@login_required
def view_event(request, owner_type, owner_id, event_id):
    """Return the event with event_id if the current user has permission to
    view the calendar to which the event belongs"""
    # Like before, get the request's context.
    context = RequestContext(request)

    user = request.user
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'GET':
        verified_obj = verified_calendar(owner_type, owner_id, user)
        if isinstance(verified_obj, Calendar):
            calendar = verified_obj
        else:
            return verified_obj

        event = Event.objects.get(id=int(event_id))

        #If the event mentioned doesn't belong to the calendar
        if not (event.cal.id == calendar.id):
            return HttpResponse('You do not have permission to view this event')

    else:
        return render_to_response('/main/', {}, context)

    # Render the template depending on the context.
    return render_to_response(
           'scheduler/view_event.html', {'event': event},
           context)

@login_required
def update_event(request, owner_type, owner_id, event_id):
    """Return the event with event_id if the current user has permission to
    view the calendar to which the event belongs"""
    # Like before, get the request's context.
    context = RequestContext(request)

    user = request.user

    verified_obj = verified_calendar(owner_type, owner_id, user)
    if isinstance(verified_obj, Calendar):
        calendar = verified_obj
    else:
        return verified_obj

    event = Event.objects.get(id=int(event_id))

    #If the event mentioned doesn't belong to the calendar
    if not (event.creator.id == user.id or event.cal.id == calendar.id):
        return HttpResponse('You do not have permission to edit this event')

    event_added = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        event_form = EventForm(data=request.POST, instance=event)
        if (event_form.is_valid()):
            e = event_form.save(commit=False)
            e.save()
            event_added = True
    else:
        event_form = EventForm(instance=event)

    # Render the template depending on the context.
    return render_to_response('scheduler/update_event.html',
           {'event_form': event_form, 'user' : user,
           'event_added': event_added},
           context)
