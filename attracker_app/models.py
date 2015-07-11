from django.db import models

class Segment(models.Model):
    start_mile = models.FloatField('Starting Nobo mile post', default=0)
    end_mile = models.FloatField('Ending Nobo mile post', default=0)
    date = models.DateTimeField('Date segment was hiked')

    @property
    def distance(self):
        return self.end_mile - self.start_mile

    def __str__(self):
        return "Start @ mile {} for {} miles".format(self.start_mile, self.distance)

class AppalachianTrail(models.Model):
    miles = models.FloatField('Total number of miles in AT', default=2184.2)

    def __str__(self):
        return str(self.miles)
