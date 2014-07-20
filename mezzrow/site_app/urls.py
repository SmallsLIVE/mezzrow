from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()


class StaticPageView(TemplateView):
    def get_template_names(self):
        return ["{0}.html".format(self.kwargs['template_name'])]


urlpatterns = patterns('',
    url(r'^static_page/(?P<template_name>[A-Za-z_-]*)/$', StaticPageView.as_view(), name="static_page"),
    url(r'^events/(?P<pk>\d+)-(?P<page_slug>[-\w]+)/edit/$', 'site_app.views.event_edit', name='event_edit'),
    url(r'^events/(?P<pk>\d+)-(?P<slug>[-\w]+)', 'site_app.views.event_view', name='event_detail'),
    url(r'^events/add/', 'site_app.views.event_add', name='event_add'),
    url(r'^month/$', 'site_app.views.month_view', name='events_month'),
    url(r'^year/$', 'site_app.views.year_view', name='events_year'),
    url(r'^artists/add/$', 'site_app.views.artist_add', name='artist_add'),
    url(r'^artists/(?P<pk>\d+)/instrument_ajax/$', 'smallslive.artists.views.artist_instrument_ajax', name='artist_intrument_ajax'),
    url(r'^contact/$', 'site_app.views.contact_view', name='contact'),
    url(r'^about/$', 'site_app.views.about_view', name='about'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)

urlpatterns += staticfiles_urlpatterns()
