from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main.models import UserProfile, Student
from main.utils import render_permission_denied
from scheduler.models import Calendar, Event
from scheduler.forms import EventForm
import json

def verified_calendar(context, owner_type, owner_id, user):
    """Return a calendar owned by owner_id only if the current user has
    permission to view the calendar
    If the owner_type is a school or a course, ensure that the user is
    enrolled"""

    if (owner_type == 'user'):
        if (user.id == int(owner_id)):
            calendar = UserProfile.objects.get(user=user).cal
            edit_priv = True
        else:
            #return HttpResponse('Sorry, this is not your own profile!')
            return render_permission_denied(context, 'access this user\'s calendar')
    elif (owner_type == 'school'):
        profile = UserProfile.objects.get(user=user)
        if (profile.school.id == int(owner_id)):
            calendar = profile.school.cal
            edit_priv = profile.school.admin.id == user.id
        else:
            #return HttpResponse('Sorry, this is not your school!')
            return render_permission_denied(context, 'access this school\'s calendar')
    elif (owner_type == 'course'):
        profile = UserProfile.objects.get(user=user)
        course = profile.courses.filter(id=int(owner_id))[:1]
        # If the user is enrolled in a course and the school
        if course and course[0].school.id == profile.school.id:
            calendar = course[0].cal      
            
            #If student
            if (Student.objects.filter(user=user)):
                edit_priv = False
                if (course[0].student_admins.filter(id=int(profile.id))):
                    edit_priv = True
                
            #If teacher
            elif (course[0].creator.id == profile.user.id) :
                edit_priv = True
                
            else:
                edit_priv = False
        else:
            return render_permission_denied(context, ' access this course\'s calendar')
    return (calendar, edit_priv)



@login_required
def calendar_view_basic(request, owner_type, owner_id):
    """Return a calendar owned by owner_id only if the current user has
    permission to view the calendar"""

    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'GET':
        verified_obj = verified_calendar(context, owner_type, owner_id, user)
        if not isinstance(verified_obj, HttpResponse):
            calendar, edit_priv = verified_obj
            events = calendar.event_set.all()
        else:
            return verified_obj

        response_object = {'calendar' : calendar, 'events': events,
                    'edit_priv': edit_priv, 'owner_type': owner_type,
                   }

        if owner_type == "user":
            
            # send school calendar
            profile_school = user_profile.getSchool()
            response_object['school'] = profile_school
            if profile_school != None:
                response_object['school_events'] = profile_school.cal.event_set.all()
           
            # send course calendars
            profile_courses = user_profile.courses.all()
            course_calendars = []
            for course in profile_courses:
                course_calendars.append({'course': course, 'events': course.cal.event_set.all()})
            response_object['course_calendars'] = course_calendars;
        return render_to_response('scheduler/calendar_basic.html',
                    response_object, context)
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('/login.html', {}, context)

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
        verified_obj = verified_calendar(context, owner_type, owner_id, user)
        if not isinstance(verified_obj, HttpResponse):
            calendar, edit_priv = verified_obj
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
    edit_priv = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'GET':
        verified_obj = verified_calendar(context, owner_type, owner_id, user)
        if not isinstance(verified_obj, HttpResponse):
            calendar, edit_priv = verified_obj
        else:
            return verified_obj

        event = Event.objects.get(id=int(event_id))

        #If the event mentioned doesn't belong to the calendar
        if not (event.cal.id == calendar.id):
            return render_permission_denied(context, 'view this event')

    else:
        return render_to_response('/', {}, context)

    # Render the template depending on the context.
    return render_to_response(
           'scheduler/view_event.html', {'event': event, 'edit_priv': edit_priv},
           context)

@login_required
def update_event(request, owner_type, owner_id, event_id):
    """Return the event with event_id if the current user has permission to
    view the calendar to which the event belongs"""
    # Like before, get the request's context.
    context = RequestContext(request)

    user = request.user

    verified_obj = verified_calendar(context, owner_type, owner_id, user)
    if not isinstance(verified_obj, Calendar):
        calendar = verified_obj
    else:
        return verified_obj

    event = Event.objects.get(id=int(event_id))

    #If the event mentioned doesn't belong to the calendar
    if not (event.creator.id == user.id or event.cal.id == calendar.id):
        #return HttpResponse('You do not have permission to edit this event')
        return render_permission_denied(context, 'edit this event')

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
