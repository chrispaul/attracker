from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from datetime import date, timedelta
from django.utils.safestring import mark_safe
from django.utils.html import escapejs
import json
import os

from .models import AppalachianTrail, Segment, Hiker


def index(request):
    hikers = Hiker.objects.order_by('trail_name')
    context = {'hikers': hikers}
    return render(request, 'attracker/index.html', context)

def hiker(request, hiker_id):
    hiker = get_object_or_404(Hiker, pk=hiker_id)
    segments = hiker.segment_set.all().order_by('start_mile')
    google_maps_browser_key = os.environ['GOOG_MAP_API_KEY']
    #CP TODO rm: White Mtn Hostel & North
    polylines = [
        { 'color': 'blue', 'coordinates': [
            {'lat': 44.40016162702151, 'lng': -71.11198885103762},
            {'lat': 44.40016017265461, 'lng': -71.1119944870284},
            {'lat': 44.40026011006432, 'lng': -71.11208371888176},
            {'lat': 44.40037432416757, 'lng': -71.11216938128825},
            {'lat': 44.4004314312886, 'lng': -71.11222648973927},
        ]},
        { 'color': 'yellow', 'coordinates': [
            {'lat': 44.40039930901872, 'lng': -71.1122943069697},
            {'lat': 44.40092754917721, 'lng': -71.11267621835199},
            {'lat': 44.40158784946722, 'lng': -71.11317234646766},
            {'lat': 44.40224814975794, 'lng': -71.11366847458358},
    ]}]
    mid =  {'lat': 44.40039930901872, 'lng': -71.1122943069697}
    return render(request, 'attracker/hiker.html', {
        'hiker': hiker, 
        'segments': segments, 
        'google_maps_browser_key': google_maps_browser_key, 
        'polylines': mark_safe(escapejs(json.dumps(polylines))),
        'mid': mark_safe(escapejs(json.dumps(mid))) 
    })

def segment_add(request, hiker_id):
    if request.method == 'POST':
        return segment_add_post(request, hiker_id)
    elif request.method == 'GET':
        return segment_add_get(request, hiker_id)
    else:
        return render(request, 'attracker/segment_add.html', {
            'error_message': "Internal error: Invalid method {0}".format(request.method),
        })

def segment_add_get(request, hiker_id):
    hiker = get_object_or_404(Hiker, pk=hiker_id)
    next_date = hiker.last_segment_date+timedelta(days=1)
    return render(request, 'attracker/segment_add.html', {
        'hiker': hiker,
        'next_date': next_date
    })

def segment_add_post(request, hiker_id):
    hiker = get_object_or_404(Hiker, pk=hiker_id)
    try:
        s = Segment(
                hiker = hiker, 
                date = request.POST['date'],
                start_mile = request.POST['start_mile'] or 0.0, 
                end_mile = request.POST['end_mile'] or 0.0, 
                description = request.POST['description'], 
                video_url = request.POST['video_url'], 
                picture_url = request.POST['picture_url'], 
                additional_miles = request.POST['additional_miles'] or 0.0 #TODO: what is the idiomatic way to make sure value is not ''?
                )
        s.save()
    except:
        import sys
        e = sys.exc_info()[0]
        return render(request, 'attracker/segment_add.html', {
            'error_message': "Internal error {0}".format(e),
        })
    else:
        return HttpResponseRedirect(reverse('hiker', args=(hiker.id,)))

def segment_delete(request, hiker_id, segment_id):
    start_mile = 0
    hiker = get_object_or_404(Hiker, pk=hiker_id)
    segment = get_object_or_404(Segment, pk=segment_id)
    try:
        if (hiker.id != segment.hiker.id):
            # Redisplay the hiker form.
            return render(request, 'attracker/index.html', {
                'error_message': "Internal delete error:{0}:{1}:{2}".format(hiker_id, segment.hiker.id, segment_id)
            })
        segment.delete()
    except:
        # Redisplay the hikers form.
        return render(request, 'attracker/index.html', {
            "Internal delete error: {0}/{1}".format(hiker_id, segment_id),
        })
    return HttpResponseRedirect(reverse('hiker', args=(hiker.id,)))


def segment_edit(request, hiker_id, segment_id):
    hiker = get_object_or_404(Hiker, pk=hiker_id)
    segment = get_object_or_404(Segment, pk=segment_id)
    if request.method == 'POST':
        return segment_edit_post(request, hiker, segment)
    elif request.method == 'GET':
        return segment_edit_get(request, hiker, segment)
    else:
        return render(request, 'attracker/index.html', {
            'error_message': "Internal error: Invalid method {0}".format(request.method),
        })

def segment_edit_get(request, hiker, segment):
    return render(request, 'attracker/segment_edit.html', {'hiker': hiker, 'segment': segment})

def segment_edit_post(request, hiker, segment):
    #try:
    segment.date = request.POST['date']
    segment.start_mile = float(request.POST['start_mile'])
    segment.end_mile = float(request.POST['end_mile'])
    segment.description = request.POST['description']
    segment.video_url = request.POST['video_url']
    segment.picture_url = request.POST['picture_url']
    segment.additional_miles = float(request.POST['additional_miles'])
    segment.save()
    '''except:
        import sys
        e = sys.exc_info()[0]
        return render(request, 'attracker/index.html', {
            'error_message': "Internal error {0}".format(e),
        })
    else:
    '''
    return HttpResponseRedirect(reverse('hiker', args=(hiker.id,)))


