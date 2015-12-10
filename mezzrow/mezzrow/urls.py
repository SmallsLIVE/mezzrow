from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.templatetags.staticfiles import static
from oscar.app import shop
from paypal.express.dashboard.app import application as express_app
from paypal.payflow.dashboard.app import application as payflow_app
from django.contrib import admin
from oscar_apps.checkout.views import PaypalExpressSuccessResponseView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/todays-events/$',
        'site_app.api.todays_events', name="todays_events"),
    url(r'^checkout/paypal/preview/(?P<basket_id>\d+)/$',
        PaypalExpressSuccessResponseView.as_view(preview=True), name='paypal-success-response'),
    url(r'^checkout/paypal/place-order/(?P<basket_id>\d+)/$', PaypalExpressSuccessResponseView.as_view(),
        name='paypal-place-order'),
    (r'^checkout/paypal/', include('paypal.express.urls')),
    (r'^dashboard/paypal/express/', include(express_app.urls)),
    (r'^dashboard/paypal/payflow/', include(payflow_app.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^accounts/', include('allauth.urls', app_name="allauth")),
    url(r'', include('site_app.urls')),
    url(r'', include(shop.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
