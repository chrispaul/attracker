from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import AppalachianTrail, Segment, Hiker


def index(request):
    hikers = Hiker.objects.order_by('trail_name')
    context = {'hikers': hikers}
    return render(request, 'attracker/index.html', context)

def hiker(request, hiker_id):
    hiker = get_object_or_404(Hiker, pk=hiker_id)
    return render(request, 'attracker/hiker.html', {'hiker': hiker})

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
    try:
        hiker = get_object_or_404(Hiker, pk=hiker_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'attracker/segment_add.html', {
            'error_message': "No such hiker with ID {0}".format(hiker_id),
        })
    else:
        return render(request, 'attracker/segment_add.html', {'hiker': hiker})

def segment_add_post(request, hiker_id):
    try:
        hiker = get_object_or_404(Hiker, pk=hiker_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'attracker/segment_add.html', {
            'error_message': "No such hiker with ID {0}".format(hiker_id),
        })
    else:
        date = request.POST['date']
        start_mile = request.POST['start_mile']
        debug_info = "You're adding a segment to hiker {0}, date={1}, start={2}".format(hiker.trail_name, date, start_mile) # TODO
        return render(request, 'attracker/hiker.html', {'hiker': hiker, 'debug_info':debug_info})
