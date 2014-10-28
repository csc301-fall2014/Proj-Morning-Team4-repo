from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
#from school.forms import SchoolProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def add_school(request):
     # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

     # If it's a HTTP POST, we're interested in processing form data.
    
    # Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.
    


        
    # Render the template depending on the context.
    return render_to_response(
            'school/add_school.html',
            {}, context)
            


