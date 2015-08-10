from django.db import models
from django.contrib.auth.models import User
import datetime

class Hiker(models.Model):
    user = models.OneToOneField(User)
    trail_name = models.CharField('Trail name', max_length=200, null=True, blank=True)

    def num_segments(self):
        return self.segment_set.count()
    num_segments.short_description = 'Number of segments hiked'

    number_segments = property(num_segments)

    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return "{} (segments: {})".format(self.trail_name, self.number_segments)

class Segment(models.Model):
    start_mile = models.FloatField('Starting Nobo mile post', default=0)
    end_mile = models.FloatField('Ending Nobo mile post', default=0)
    description = models.CharField('Comments on the section hiked', max_length=2000, null=True, blank=True)
    video_url = models.CharField('Link to video from the section', max_length=300, null=True, blank=True)
    picture_url = models.CharField('Link to pictures', max_length=300, null=True, blank=True)
    additional_miles = models.FloatField('Non-AT miles hiked with the segment', default=0)
    date = models.DateField('Date segment was hiked')
    hiker = models.ForeignKey(Hiker)

    @property
    def distance(self):
        return round(self.end_mile - self.start_mile,1)

    def __str__(self):
        return "Start @ mile {0} for {1:.1f} miles".format(self.start_mile, self.distance)

class AppalachianTrail(models.Model):
    miles = models.FloatField('Total number of miles in AT', default=2184.2)

    def __str__(self):
        return str(self.miles)
