from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from datetime import date, timedelta
from django.utils.safestring import mark_safe
from django.utils.html import escapejs
import json
import os
from . import at_coordinates
from . import at_features

from .models import AppalachianTrail, Segment, Hiker


def index(request):
    hikers = Hiker.objects.order_by('trail_name')
    context = {'hikers': hikers}
    return render(request, 'attracker/index.html', context)

def build_polylines(segments):
    polylines = []

    # If first segment is after Springer, let's paint starting with yellow, else blue
    HIKED_COLOR = 'blue'
    TO_HIKE_COLOR = 'yellow'  # The yellow brick road
    segment_i = 0
    # TODO: handle hiker with NO segments hiked: if segments.length... else segment = Segment(start_mile=settings.AT_TRAIL_MILES+1...)
    segment = segments[segment_i] # Start at southernmost segment hiked
    polyline = {'color': HIKED_COLOR, 'coordinates': []} # Build 1st polyline
    if segment.start_mile > 0: # If hiker's first segment
        polyline['color'] = TO_HIKE_COLOR
    hiking_in_segment = False

    for coordinate in at_coordinates.COORDINATES:
        # If the coordinates line has a mile and it matches the current segment
        if (coordinate.get('mile') == segment.start_mile):
            hiking_in_segment = True
            # if we are transitioning from hiked to unhiked
            if (polyline['color'] == TO_HIKE_COLOR):
                if len(polyline['coordinates']):
                    # Break off the unhiked polyline, and start a new hiked polyline
                    polylines.append(polyline) # Add the polyline with the unhiked color
                    polyline = {'color': HIKED_COLOR, 'coordinates': []} # Start a new hiked line
                else: # Empty polyline: just change color.
                    polyline['color'] = HIKED_COLOR
            # TODO Hackzone due to having very few coodinate['mile'] entries: advance segment to last segment if next segment has starts at this segment's end
            while (segment_i < len(segments)-1) and (segments[segment_i].end_mile == segments[segment_i+1].start_mile):
                segment_i += 1
                segment = segments[segment_i]
        elif (coordinate.get('mile') == segment.end_mile):
            hiking_in_segment = False
            if segment_i < len(segments)-1:
                segment_i += 1 # Advance to next segment
                segment = segments[segment_i]
        # We at a point that doesn't correspond to a segment start or end.
        # If we we are not in a segment and we think we are hiking, transition to TO_HIKE_COLOR
        elif not hiking_in_segment and polyline['color'] == HIKED_COLOR: 
            # Break off the hiked polyline, and start a new unhiked polyline
            polylines.append(polyline) # Add the polyline with the hiked color
            polyline = {'color': TO_HIKE_COLOR, 'coordinates': []} # Start a new unhiked line
            hiking_in_segment = False
        polyline['coordinates'].append(coordinate) # Add the line to the polyline.
    if len(polyline['coordinates']):
        # Break off the unhiked polyline, and start a new hiked polyline
        polylines.append(polyline) # Add the polyline with the unhiked color
    return polylines

def hiker(request, hiker_id):
    # To display markers for each polyline in the trail, append ?markers=1 as the querystring.
    display_markers = int(request.GET.get('markers',0))
    hiker = get_object_or_404(Hiker, pk=hiker_id)
    segments = hiker.segment_set.all().order_by('start_mile')
    google_maps_browser_key = os.environ['GOOG_MAP_API_KEY']
    mid = at_coordinates.MID
    # Build the blue & yellow polylines from the segments hiked and the AT coordinates.
    polylines = build_polylines(segments)

    return render(request, 'attracker/hiker.html', {
        'hiker': hiker, 
        'segments': segments, 
        'google_maps_browser_key': google_maps_browser_key, 
        'polylines': mark_safe(escapejs(json.dumps(polylines))),
        'mid': mark_safe(escapejs(json.dumps(mid))),
        'features': mark_safe(escapejs(json.dumps(at_features.FEATURES))), # Shelters & peaks
        'display_markers': display_markers
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


