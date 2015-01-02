from django.conf.urls import patterns, include, url
from main import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csc301_calendar_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.registration, name='registration'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^edit-profile/$', views.user_update, name='edit-profile'),
    url(r'^event_notifications/$', views.event_notifications, name='notifications'),
    url(r'^instructor_admin_requests/$', views.instructor_admin_requests, name='admin requests'),
    url(r'^student_admin_requests/$', views.student_admin_requests, name='student admin requests'),
    url(r'^delete_notifications/$', views.delete_notifications, name='delete notifications'),

)
