from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin_page$', views.admin_page),
    url(r'^register_user$', views.register_user),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^login_user$', views.login_user),
    url(r'^logout$', views.logout),
    url(r'^events$', views.events),
    url(r'^view/(?P<trip_id>\d+)$', views.view_trip),
    url(r'^events/(?P<trip_id>\d+)/cancel$', views.cancel_trip),
    url(r'^events/(?P<trip_id>\d+)/delete$', views.delete_trip),
    url(r'^events/(?P<trip_id>\d+)/join$', views.join_trip),
    url(r'^addevent$', views.add_event),
    url(r'^processtrip$', views.process_trip),
]