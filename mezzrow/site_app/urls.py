from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import TemplateView
from .sitemaps import StaticViewSitemap, EventDetailSitemap, EventListSitemap

admin.autodiscover()


class StaticPageView(TemplateView):
    def get_template_names(self):
        return ["{0}.html".format(self.kwargs['template_name'])]

sitemaps = {
    'static': StaticViewSitemap,
    'event': EventDetailSitemap,
    'event_list': EventListSitemap
}


urlpatterns = patterns('',
    url(r'^static_page/(?P<template_name>[A-Za-z_-]*)/$', StaticPageView.as_view(), name="static_page"),
    url(r'^events/(?P<pk>\d+)-(?P<slug>[-\w]+)/clone/$', 'site_app.views.event_clone', name='event_clone'),
    url(r'^events/(?P<pk>\d+)-(?P<slug>[-\w]+)/delete/$', 'site_app.views.event_delete', name='event_delete'),
    url(r'^events/(?P<pk>\d+)-(?P<slug>[-\w]+)/edit/$', 'site_app.views.event_edit', name='event_edit'),
    url(r'^events/(?P<pk>\d+)-(?P<slug>[-\w]+)', 'site_app.views.event_view', name='event_detail'),
    url(r'^events/past/', 'site_app.views.past_events', name='past_events'),
    url(r'^events/add/', 'site_app.views.event_add', name='event_add'),
    #url(r'^month/$', 'site_app.views.month_view', name='events_month'),
    #url(r'^year/$', 'site_app.views.year_view', name='events_year'),
    url(r'^artists/(?P<pk>\d+)-(?P<slug>[-\w]+)/edit/', 'site_app.views.artist_edit', name='artist_edit'),
    url(r'^artists/(?P<pk>\d+)-(?P<slug>[-\w]+)', 'site_app.views.artist_view', name='artist_detail'),
    url(r'^artists/add/$', 'site_app.views.artist_add', name='artist_add'),
    url(r'^artists/(?P<pk>\d+)/instrument_ajax/$', 'smallslive.artists.views.artist_instrument_ajax',
        name='artist_intrument_ajax'),
    url(r'^ticketing/$', 'site_app.views.ticketing_view', name='ticketing'),
    url(r'^contact/$', 'site_app.views.contact_view', name='contact'),
    url(r'^about/$', 'site_app.views.about_view', name='about'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^next/(?P<week>\d+)/$', 'site_app.views.home_view', name='next'),
    url(r'^$', 'site_app.views.home_view', name='home'),
)

urlpatterns += staticfiles_urlpatterns()
