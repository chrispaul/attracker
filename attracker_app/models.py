from django.db import models
from django.contrib.auth.models import User

class Hiker(models.Model):
    user = models.OneToOneField(User)
    trail_name = models.CharField('Trail name', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.trail_name

class Segment(models.Model):
    start_mile = models.FloatField('Starting Nobo mile post', default=0)
    end_mile = models.FloatField('Ending Nobo mile post', default=0)
    description = models.CharField('Comments on the section hiked', max_length=2000, null=True, blank=True)
    video_url = models.CharField('Link to video from the section', max_length=300, null=True, blank=True)
    picture_url = models.CharField('Link to pictures', max_length=300, null=True, blank=True)
    additional_miles = models.FloatField('Non-AT miles hiked with the segment', default=0)
    date = models.DateTimeField('Date segment was hiked')
    hiker = models.ForeignKey(Hiker)

    @property
    def distance(self):
        return self.end_mile - self.start_mile

    def __str__(self):
        return "Start @ mile {} for {} miles".format(self.start_mile, self.distance)

class AppalachianTrail(models.Model):
    miles = models.FloatField('Total number of miles in AT', default=2184.2)

    def __str__(self):
        return str(self.miles)
