from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^event/(?P<pk>\d+)-(?P<page_slug>\w+)', 'site_app.views.event_view', name='event'),
    url(r'^event/add/', 'smallslive.events.views.event_add', name='event_add'),
    url(r'^contact/$', 'site_app.views.contact_view', name='contact'),
    url(r'^about/$', 'site_app.views.about_view', name='about'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)

urlpatterns += staticfiles_urlpatterns()
