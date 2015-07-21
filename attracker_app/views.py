from django.http import HttpResponse

from .models import AppalachianTrail, Segment, Hiker

def index(request):
    hikers = Hiker.objects.order_by('trail_name')
    output = ', '.join([h.trail_name for h in hikers])
    return HttpResponse(output)

def hiker(request, hiker_id):
    return HttpResponse("You're looking at segments for hiker %s." % hiker_id)

def add_segment(request, hiker_id):
    response = "You're adding a segment to hiker %s."
    return HttpResponse(response % hiker_id)
