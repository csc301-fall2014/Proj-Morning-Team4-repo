from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

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

	