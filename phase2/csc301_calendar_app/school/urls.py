from django.conf.urls import patterns, include, url
from school import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csc301_calendar_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^search/$', views.get_schools, name='Search Schools'),
    url(r'^(?P<school_id>\w+)/$', views.view_school, name='View School'),
    url(r'^course/create/$', views.create_course, name='Create course'),
    url(r'^course/search/$', views.get_courses, name='Search courses'),
    url(r'^course/(?P<course_id>\w+)/$', views.view_course, name='View course'),
    url(r'^course/(?P<course_id>\w+)/add_student_admin/$', views.add_student_admin, name='Add Student Admin'),
    url(r'^course/(?P<course_id>\w+)/accept_student_admin/(?P<student_id>\w+)/$', views.accept_student_admin, name='Accept Student Admin'),
    url(r'^course/(?P<course_id>\w+)/request_student_admin/(?P<student_id>\w+)/$', views.request_student_admin, name='Request Student Admin'),


)
