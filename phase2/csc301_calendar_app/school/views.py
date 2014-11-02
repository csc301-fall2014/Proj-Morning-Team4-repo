from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from school.forms import SchoolProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def add_school(request):
     # Like before, get the request's context.
    context = RequestContext(request)

     # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        school_form = SchoolProfileForm(data=request.POST)


    # Render the template depending on the context.
    return render_to_response('school/add_school.html', {}, context)    
    

    


    
            


