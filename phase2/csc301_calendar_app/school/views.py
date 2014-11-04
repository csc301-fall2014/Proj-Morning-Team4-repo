from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from school.forms import SchoolProfileForm
from school.models import SchoolProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def get_schools(request):
     # Like before, get the request's context.
    context = RequestContext(request)

     # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'GET':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        schools = SchoolProfile.objects.all()


    # Render the template depending on the context.
    return render_to_response('school/search_schools.html', {'schools': schools}, context)    
    

    


    
            


