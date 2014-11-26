from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from models import Instructor, UserProfile, Student
from school.models import Course, SchoolProfile

'''
	Return a response with a template that describes a 401 permission error.
	Takes a context from the request, and text that completes the following
	sentence.
	"Sorry, you don't have permission to __________"
'''
def render_permission_denied(context, text):
	template = loader.get_template('main/permission_denied.html')
	context['access'] = text
	return HttpResponse(template.render(context), status=401)


def get_profile(user):
    try:
        user_profile = Instructor.objects.get(user=user.id)
        user_type = 'Instructor'
    except Instructor.DoesNotExist:
        try:
            user_profile = Student.objects.get(user=user.id)
            user_type = 'Student'
        except Student.DoesNotExist:
            user_profile = None
            user_type = None
    return [user_profile, user_type]

def get_owner_definition(request, owner_type, owner_id):
	owner_id = int(owner_id)
	if 'course' in owner_type:
		owner = Course.objects.filter(id = owner_id)
		if owner:
			owner_name = owner[0].code
		owner_type = "course"
	elif 'school' in owner_type:
		owner = SchoolProfile.objects.filter(id = owner_id)
		if owner:
			owner_name = owner[0].name
		owner_type = "school"
	elif 'user' in owner_type:
		owner = User.objects.filter(id = owner_id)
		if owner:
			owner_name = "Personal"
		owner_type = "user"
	else:
		owner = ""


	if (owner and owner != ""):
		return [owner[0], owner_type, owner_name]
	else:
		return ["", "", ""]
