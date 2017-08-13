from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: / # shows all hikers
    url(r'^$', views.index, name='index'),

    # ex: /5/ # shows one hiker's segments
    url(r'^(?P<hiker_id>[0-9]+)/$', views.hiker, name='hiker'),

    # ex: /5/segment/add/ # add a segment to a hiker's hike
    url(r'^(?P<hiker_id>[0-9]+)/segment/add/$', views.segment_add, name='segment_add'),

    # ex: /5/segment/add2/ # add a segment to a hiker's hike  #TODO >>Kill add, swap in add2
    url(r'^(?P<hiker_id>[0-9]+)/segment/add2/$', views.segment_add2, name='segment_add2'),

    # ex: /5/segment/3/delete/ # Delete a segment from a hiker's hike
    url(r'^(?P<hiker_id>[0-9]+)/segment/(?P<segment_id>[0-9]+)/delete/$', views.segment_delete, name='segment_delete'),

    # ex: /5/segment/3/edit/ # Edit a segment from a hiker's hike
    url(r'^(?P<hiker_id>[0-9]+)/segment/(?P<segment_id>[0-9]+)/edit/$', views.segment_edit, name='segment_edit'),
]
