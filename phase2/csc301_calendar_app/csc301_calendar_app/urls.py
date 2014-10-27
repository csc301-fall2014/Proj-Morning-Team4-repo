from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin # UNCOMMENT THIS LINE
admin.autodiscover() # UNCOMMENT THIS LINE, TOO!

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csc301_calendar_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls'),
    url(r'^', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
