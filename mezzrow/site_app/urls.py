from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^events/(?P<pk>\d+)-(?P<slug>\w+)', 'site_app.views.event_view', name='event_detail'),
    #url(r'^event/add/', 'smallslive.events.views.event_add', name='event_add'),
    url(r'^events/add/', 'site_app.views.event_add', name='event_add'),
    url(r'^artists/add/$', 'site_app.views.artist_add', name='artist_add'),
    url(r'^artists/(?P<pk>\d+)/instrument_ajax/$', 'smallslive.artists.views.artist_instrument_ajax', name='artist_intrument_ajax'),
    url(r'^contact/$', 'site_app.views.contact_view', name='contact'),
    url(r'^about/$', 'site_app.views.about_view', name='about'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)

urlpatterns += staticfiles_urlpatterns()
