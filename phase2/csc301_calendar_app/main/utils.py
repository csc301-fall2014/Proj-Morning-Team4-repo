from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def render_permission_denied(context, text):
	template = loader.get_template('main/permission_denied.html')
	context['access'] = text
	return HttpResponse(template.render(context), status=401)