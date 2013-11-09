from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import SearchView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', SearchView.as_view(), name='home'),
    url(r'^api/create_torrent$', 'tpb_mobile.views.create_torrent_record', name='create_torrent'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
