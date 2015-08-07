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



from django.http import HttpResponse

def segment_add(request, hiker_id):
    response = "You're adding a segment to hiker %s."
    return HttpResponse(response % hiker_id)
