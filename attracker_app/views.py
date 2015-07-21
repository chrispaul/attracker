from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, AT Tracker HP world. ")

def hiker(request, hiker_id):
    return HttpResponse("You're looking at segments for hiker %s." % hiker_id)

def add_segment(request, hiker_id):
    response = "You're adding a segment to hiker %s."
    return HttpResponse(response % hiker_id)
