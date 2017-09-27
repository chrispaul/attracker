from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from django.db.models import Max

class Hiker(models.Model):
    user = models.OneToOneField(User)
    trail_name = models.CharField('Trail name', max_length=200, null=True, blank=True)

    def num_segments(self):
        return self.segment_set.count()
    num_segments.short_description = 'Number of segments hiked'
    number_segments = property(num_segments)

    def last_segment_date(self):
        return self.segment_set.aggregate(Max('date'))['date__max']
    last_segment_date.short_description = 'Date of the last segment hiked'
    last_segment_date = property(last_segment_date)

    def last_mile(self):
        return self.segment_set.aggregate(Max('end_mile'))['end_mile__max']
    last_mile.short_description = 'Maximum mile hiked'
    last_mile = property(last_mile)

    def miles_hiked(self):
        return round(sum([s.distance for s in self.segment_set.all()]),1)
    miles_hiked.short_description = 'Total miles hiked'
    miles_hiked = property(miles_hiked)

    def percent_hiked(self):
        return round(100.0*self.miles_hiked/settings.AT_TRAIL_MILES,1)
    percent_hiked.short_description = 'Total miles hiked'
    percent_hiked = property(percent_hiked)

    def miles_to_go(self):
        return round(settings.AT_TRAIL_MILES - sum([s.distance for s in self.segment_set.all()]), 1)
    miles_to_go.short_description = 'Total miles remaining on AT'
    miles_to_go = property(miles_to_go)


    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return "{} (segments: {})".format(self.trail_name, self.number_segments)


class Segment(models.Model):
    """ A hike is composed of multiple segments. Segments have start and end miles.
    start_mile and end_mile are foreign keys into Point.mile. 
    start_mile could be > or < end_mile (in the future).
    Segments may overlap (in the future).
    """
    start_mile = models.FloatField('Starting Nobo mile post', default=0)
    end_mile = models.FloatField('Ending Nobo mile post', default=0)
    #TODO Change to decimal? start_mile2 = models.DecimalField(max_digits=4, decimal_places=1)
    #TODO end_mile2 = models.DecimalField(max_digits=4, decimal_places=1)
    description = models.CharField('Comments on the section hiked', max_length=2000, null=True, blank=True)
    video_url = models.CharField('Link to video from the section', max_length=300, null=True, blank=True)
    picture_url = models.CharField('Link to pictures', max_length=300, null=True, blank=True)
    additional_miles = models.FloatField('Non-AT miles hiked with the segment', blank=True, default=0)
    date = models.DateField('Date segment was hiked')
    hiker = models.ForeignKey(Hiker)

    @property
    def distance(self):
        return round(self.end_mile - self.start_mile,1)

    def __str__(self):
        return "Start @ mile {0} for {1:.1f} miles".format(self.start_mile, self.distance)


class AppalachianTrail(models.Model):
    miles = models.FloatField('Total number of miles in AT', default=settings.AT_TRAIL_MILES)

    def __str__(self):
        return str(self.miles)


class Point(models.Model):
    """ Point on (or off) the trail. Miles are always in tenths. """
    mile = models.FloatField('Miles from Springer', default=0)
    lat = models.FloatField('Latitude (degrees with fraction, e.g. 34.62673', default=0)
    lon = models.FloatField('Longitude (degrees with fraction, e.g. -84.193656', default=0)
    description = models.CharField('Description of point')

    @property
    def sobo_mile(self):
        return round((settings.AT_TRAIL_MILES - nobo_mile),1)  # Miles from Katahdin

    def miles_to_trail(self):
        ''' For points not on trail, number of miles to the nearest point on trail as the crow flies'''
        return 0  #TODO >>>>>>>

    def __str__(self):
        return "mile={mile}".format(mile=self.mile)


'''
at_coordinates.py
COORDINATES = [
  {'lat': 34.626693161734536, 'lng': -84.19382841822977, 'mile': 0, 'description': 'Springer Mountain'},

at_features.py:
FEATURES = [
  {"mile": 0.0, "type": "FEATURE", "name": "Mile 0.0: Springer Mt (3782 ft): 34.62673/-84.193656", "lat": 34.62673, "lon": -84.193656},
'''
