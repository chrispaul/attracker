from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /attracter/ # shows all hikers
    url(r'^$', views.index, name='index'),

    # ex: /attracker/5/ # shows one hiker's segments
    url(r'^(?P<hiker_id>[0-9]+)/$', views.hiker, name='hiker'),

    # ex: /attracker/5/segment/add/ # add a segment to a hiker's hike
    url(r'^(?P<hiker_id>[0-9]+)/segment/add/$', views.segment_add, name='segment_add'),

    # ex: /attracker/5/segment/3/delete/ # Delete a segment from a hiker's hike
    url(r'^(?P<hiker_id>[0-9]+)/segment/(?P<segment_id>[0-9]+)/delete/$', views.segment_delete, name='segment_delete'),
]
