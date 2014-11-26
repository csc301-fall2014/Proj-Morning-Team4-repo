#from django.shortcuts import render
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.forms import UserForm, UserProfileForm, UserUpdateForm, UserTypeForm
from main.models import UserProfile, Student, Instructor
from main.utils import render_permission_denied, get_profile
from school.models import SchoolProfile, Course
from scheduler.models import Calendar
from notifications.models import Notification

from django.http import JsonResponse
import json as simplejson

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    context_dict = {
    }

    if request.user.id:
        profile = get_profile(request.user)
        user_profile = profile[0]
        user_type = profile[1]

        if 'Instructor' in user_type:
            context_dict['is_instructor'] = True
            context_dict['courses'] = Course.objects.filter(creator=request.user.id)
        else:
            context_dict['is_instructor'] = False
            context_dict['courses'] =  user_profile.courses.all()

        context_dict['user_profile'] =  user_profile

    return render_to_response('main/main.html', context_dict, context)


#(Source : http://www.tangowithdjango.com/book/chapters/login.html)
def registration(request):
     # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

     # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        user_type_form = UserTypeForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid() and user_type_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            nickname = profile_form.cleaned_data['nickname']

            # Now sort out the Student instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.

            user_type = user_type_form.cleaned_data['user_type']
            user_type = int(user_type)
            #user_type = 1
            if user_type:
                profile = Student(nickname=nickname)
            else:
                profile = Instructor(nickname=nickname)
            profile.user = user

            # Add the personal calendar for the user
            calendar = Calendar( name = user.username + "'s personal calendar")
            calendar.save()
            profile.cal = calendar
            profile.school = None
            # Now we save the Student model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors, user_type_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        user_type_form = UserTypeForm()

    # Render the template depending on the context.
    return render_to_response(
            'main/register.html',
            {'user_form': user_form, 'profile_form': profile_form,
            'user_type_form': user_type_form,
            'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_permission_denied(context,
            ' proceed with registration since invalid login details were supplied')

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('main/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

@login_required
def user_update(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    user = request.user
    user_profile = UserProfile.objects.get(user=user.id)
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=user)
        profile_form = UserProfileForm(data=request.POST, instance=user)
        if (user_form.is_valid() and profile_form.is_valid()):
            user_form.save()
            profile_form.save()
        return HttpResponseRedirect('/')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)
        return render_to_response(
            'main/edit_profile.html',
            {'user_form': user_form, 'profile_form': profile_form},
            context)

@login_required
def event_notifications(request):

    context = RequestContext(request)
    result = []

    # All event notifications for current user
    notifications = Notification.objects.filter(user__id=request.user.id,
                                        notification_type__contains='event')
    for notification in notifications:

        # get the notification type
        if "new" in notification.notification_type:
            notif_type = "new"
        else:
            notif_type = "update"


        notif = {'notify_id'    : notification.id,
                    'type'      : notif_type,
                    'owner_type': notification.owner_type,
                    'owner_name': notification.owner_name,
                    'owner_id'  : notification.owner_id,
                    "event_id"  : notification.content_object.id,
                    "event_name": notification.content_object.name,
                    'event_date': notification.content_object.start.strftime('%a. %b. %d, %I:%M %p')}

        result.append(notif)

    return HttpResponse(simplejson.dumps(result), content_type='application/json')

@login_required
def instructor_admin_requests(request):

    context = RequestContext(request)
    result = []

    # All event notifications for current user
    notifications = Notification.objects.filter(user__id=request.user.id,
                                        notification_type__contains='requested_admin')
    for notification in notifications:

        notif = {   'notify_id' : notification.id,
                    'type'      : notification.notification_type,
                    'owner_type': notification.owner_type,
                    'owner_name': notification.owner_name,
                    'owner_id'  : notification.owner_id,
                    "event_id"  : notification.content_object.id,
                    "event_name": notification.content_object.username}

        result.append(notif)

    return HttpResponse(simplejson.dumps(result), content_type='application/json')
