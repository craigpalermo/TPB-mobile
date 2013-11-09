from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import SearchView, QueueView
from api.utils import create_torrent_record, delete_torrent_record, retrieve_queue
from authentication.views import LoginView, logout_view
admin.autodiscover()

urlpatterns = patterns('tpb_mobile.views',
    # Examples:
    url(r'^$', SearchView.as_view(), name='home'),
    url(r'^queue/$', QueueView.as_view(), name='queue'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('api.utils',
    url(r'^api/create_torrent/$', create_torrent_record, name='create_torrent'),
    url(r'^api/delete_torrent/(?P<torrent_id>\d*)/$', delete_torrent_record, name='delete_torrent'),
    url(r'^api/retrieve_queue/(?P<user_id>\d*)/$', retrieve_queue, name='retrieve_queue')
)

urlpatterns += patterns('authentication.views',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout')
)
