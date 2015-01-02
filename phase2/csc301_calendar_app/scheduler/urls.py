from django.conf.urls import patterns, include, url
from scheduler import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csc301_calendar_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.calendar_view_basic, name='calendar_basic'),
    url(r'^add/$', views.add_event, name='add_event'),
    url(r'^event/(?P<event_id>\w+)/$', views.view_event, name='view_event'),
    url(r'^event/(?P<event_id>\w+)/update/$', views.update_event, name='update_event')

)
