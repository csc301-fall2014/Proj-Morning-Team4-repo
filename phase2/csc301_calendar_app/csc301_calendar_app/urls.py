from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin # UNCOMMENT THIS LINE
admin.autodiscover() # UNCOMMENT THIS LINE, TOO!

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csc301_calendar_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls'),
    url(r'^', include('main.urls')),
#   url(r'^main/', include('main.urls')),
    url(r'^(?P<owner_type>(user|school|course){1})/(?P<owner_id>\w+)/calendar/',
            include('scheduler.urls', namespace='scheduler')),
    url(r'^school/', include('school.urls', namespace='school')),
	url(r'^accounts/', include('main.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
)  + staticfiles_urlpatterns() 

if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
