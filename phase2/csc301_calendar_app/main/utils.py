from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from models import Instructor, UserProfile, Student

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
    except Instructor.DoesNotExist:
        try:
            user_profile = Student.objects.get(user=user.id)
        except Student.DoesNotExist:
            user_profile = None
    return user_profile
