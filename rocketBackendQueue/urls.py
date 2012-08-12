from django.conf.urls import patterns, include, url
from django.contrib import admin
from rocketBackendQueue import settings

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'rocketBackendQueue.views.home', name='home'),
    # url(r'^rocketBackendQueue/', include('rocketBackendQueue.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )