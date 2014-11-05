from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from school.forms import SchoolProfileForm
from school.models import SchoolProfile
from main.models import UserProfile
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

@login_required
def view_school(request, school_id):

    """Return all the courses owned by school_id and the school object.
    Also return if the current user is eligible to be enroled in to school
    with school_id, the current school the user is enrolled"""

    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    user = request.user
    eligible = False
    enrolled = False
    school = SchoolProfile.objects.get(id=int(school_id))
    if (school):
        courses = school.course_set.all()
        user_school = UserProfile.objects.get(user=user).school
        eligible = school.validate_user_email(user.email)

        if request.method == 'POST':
            #If the user wants to post, then he/she must have clicked enrol
            # button in the school
            if (eligible):
                profile = UserProfile.objects.get(user=user)
                profile.school = school
                profile.save()
                enrolled = True
            else:
                return HttpResponse("Don't belong in this school!")

        return render_to_response('school/school_view.html',
            {'school' : school, 'courses': courses, 'enrolled': enrolled,
                'eligible':eligible, 'current_school': user_school},
                context)
    else:
        return HttpResponse("No Such school exists")
