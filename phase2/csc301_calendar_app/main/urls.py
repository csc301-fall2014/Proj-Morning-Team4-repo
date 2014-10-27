from django.conf.urls import patterns, include, url
from main import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csc301_calendar_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^main', views.index, name='index'),
    url(r'^register/', views.registration, name='registration'),
)
