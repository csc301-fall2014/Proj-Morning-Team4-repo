from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from school.forms import SchoolProfileForm, CourseForm, StudentAdminForm
from school.models import SchoolProfile, Course
from main.models import UserProfile
from scheduler.models import Calendar
from main.utils import render_permission_denied, get_profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
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

    school = SchoolProfile.objects.filter(id=int(school_id))[:1]
    if (school):
        school = school[0]
        courses = school.course_set.all()
        user_school = UserProfile.objects.get(user=user).school

        eligible = school.validate_user_email(user.email)
        if (user_school):  
            enrolled = school.id == user_school.id

        if request.method == 'POST':
            #If the user wants to post, then he/she must have clicked enrol
            # button in the school
            if (eligible):
                profile = UserProfile.objects.get(user=user)
                profile.school = school
                profile.save()
                enrolled = True
            else:
                return render_permission_denied(context, 'enrol in this school')

        return render_to_response('school/school_view.html',
            {'school' : school, 'courses': courses, 'enrolled': enrolled,
                'eligible': eligible, 'current_school': user_school},
                context)
    else:
        # TODO: this is not a permission denied! This is a not found!!!!!!
        return render_permission_denied(context, 'view non existing school')

@login_required
def create_course(request):
    """ Add a course to the calendar belonging to the school
    in which the current user is enrolled in"""

     # Like before, get the request's context.
    context = RequestContext(request)
    course_added = False

    user = request.user
    profile = get_profile(user)

    if 'Instructor' in profile[1]:
        school = UserProfile.objects.get(user=user).school
        if not school:
            return render_permission_denied(context,
                'create courses. Enrol in a school first.')
    else:
        #return HttpResponse("You don't have permission to create courses!")
        return render_permission_denied(context, 'create courses')
     # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        # Attempt to grab information from the raw form information.
        course_form = CourseForm(data=request.POST)
        if course_form.is_valid():
            # Save the event's form data to the database.
            course = course_form.save(commit=False)
            course.school = school
            course.creator = user

            # Add the personal calendar for the user
            calendar = Calendar( name = course.code + " Calendar")
            calendar.save()
            course.cal = calendar

            course.save()

            course_added = True
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print course_form.errors

    # Not a HTTP POST, so we render our form using the EventForm.
    # These forms will be blank, ready for user input.
    else:
        course_form = CourseForm()

    # Render the template depending on the context.
    return render_to_response(
            'school/create_course.html', {'course_form': course_form, 'user' : user,
            'course_added': course_added, 'school': school},
            context)

@login_required
def get_courses(request):
    """ Give a list of courses which is offered by the school in which the
    user is enrolled in"""

    # Like before, get the request's context.
    context = RequestContext(request)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'GET':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_school = UserProfile.objects.get(user=request.user).school
        if user_school:
            courses = Course.objects.filter(school_id=user_school.id)
        else:
            return render_permission_denied(context, 'view courses. Please enrol in a school first')

    # Render the template depending on the context.
    return render_to_response('school/search_courses.html', {'courses': courses}, context)

@login_required
def view_course(request, course_id):

    """Return a course given a course id. If the user choses to enrol in the
    course, then add a course relation between the course and the user"""

    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    user = request.user
    eligible = False
    enrolled = False
    is_instructor = False
    course = Course.objects.filter(id=int(course_id))[:1]
    if (course):
        course = course[0]
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.school:
            eligible = course.school.id == user_profile.school.id

        relation = user_profile.courses.filter(id=course.id)[:1]
        if relation:
            enrolled = True
        
        is_instructor = course.creator.id == user_profile.user.id
    
        if request.method == 'POST':
            #If the user wants to post, then he/she must have clicked enrol
            # button in the school
            if (eligible and not enrolled):
                user_profile.courses.add(course)
                user_profile.save()
                enrolled = True

        return render_to_response('school/course_view.html',
                {'course': course, 'enrolled': enrolled,
                    'eligible':eligible, 'is_instructor': is_instructor},
                context)
    else:
        return render_permission_denied(context, ' view non existing course')

@login_required
def add_student_admin(request, course_id):

    """ Add a student admin to the course belonging to the school
       in which the instructor is enrolled in"""
   
    # Get the request's context.
    context = RequestContext(request)
    student_admin_added = False

    user = request.user
    profile = get_profile(user)
    #If has abillity to create a course then they are an instructor
    if 'Instructor' in profile[1]:
        school = UserProfile.objects.get(user=user).school
        if not school:
            return render_permission_denied(context,
                'add admin. Enrol in a school first.')
    else:
        #return HttpResponse("You don't have permission to add a student admin!")
        return render_permission_denied(context, 'add student admin')
    
    course = Course.objects.filter(id=int(course_id))[:1]
    if (course):
        course = course[0]    
        
     # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST' and course:

        # Attempt to grab information from the raw form information.
        student_admin_form = StudentAdminForm(data=request.POST)
        if student_admin_form.is_valid():
            # Save the event's form data to the database.
            student_admin = student_admin_form.cleaned_data
            course.student_admins = student_admin['student_admins']
            student_admin_added = True
            
        # Invalid form or forms - mistakes
        # Print problems to the terminal.
        else:
            print student_admin_form.errors

    # Not a HTTP POST, so we render our form using the EventForm.
    # These forms will be blank, ready for user input.
    else:
        student_admin_form = StudentAdminForm(course)

    # Render the template depending on the context.
    return render_to_response(
            'school/add_student_admin.html', {'student_admin_form': student_admin_form, 'user' : user,
            'student_admin_added': student_admin_added, 'school': school},
            context)
