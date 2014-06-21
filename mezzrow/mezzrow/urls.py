from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from oscar.app import shop
from paypal.express.dashboard.app import application
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^event/(?P<pk>\d+)-(?P<page_slug>\w+)', 'site_app.views.event_view', name='event'),
    url(r'^contact/$', 'site_app.views.contact_view', name='contact'),
    url(r'^about/$', 'site_app.views.about_view', name='about'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    (r'^checkout/paypal/', include('paypal.express.urls')),
    (r'^dashboard/paypal/express/', include(application.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'site_app.views.home_view', name='home'),
    url(r'', include(shop.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
