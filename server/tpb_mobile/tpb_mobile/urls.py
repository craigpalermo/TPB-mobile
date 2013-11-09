from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from tpb_mobile.views import SearchView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', SearchView.as_view(), name='home'),
    # url(r'^tpb_mobile/', include('tpb_mobile.foo.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
