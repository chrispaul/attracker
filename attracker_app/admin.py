from django.contrib import admin

# Register your models here.

from .models import AppalachianTrail, Segment

admin.site.register(AppalachianTrail)


class SegmentAdmin(admin.ModelAdmin):
    #fields = ['date', 'start_mile', 'end_mile']
    fieldsets = [
        (None,               {'fields': ['date']}),
        ('Miles traveled', {'fields': ['start_mile', 'end_mile']}),
    ]

admin.site.register(Segment, SegmentAdmin)
