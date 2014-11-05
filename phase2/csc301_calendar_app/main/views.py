#from django.shortcuts import render
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from main.forms import UserForm, UserProfileForm, UserUpdateForm
from main.models import UserProfile, Student
from school.models import SchoolProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from scheduler.models import Calendar

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # I'm guessing this is where all the data base requests go, if any.
    # Should delete later
    '''
    school = "s"
    for e in Student.objects.all():
        school = e.school
        print(school)
    '''

    context_dict = {
        #'app_description' : 'super duper','school' : school
    }

    if request.user.id:
        context_dict['user_profile'] =  UserProfile.objects.get(user=request.user.id)

    #context= { 'school' : Student.objects.all()}

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

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the Student instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
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
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'main/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
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
            return HttpResponse("Invalid login details supplied.")

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
