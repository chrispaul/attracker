from django.contrib import admin

# Register your models here.

from .models import AppalachianTrail, Segment

admin.site.register(AppalachianTrail)


class SegmentAdmin(admin.ModelAdmin):
    #fields = ['date', 'start_mile', 'end_mile']
    fieldsets = [
        ('Miles traveled', {'fields': ['start_mile', 'end_mile']}),
        (None,               {'fields': ['date', 'description']}),
        ('Other info', {'fields': ['additional_miles', 'video_url', 'picture_url'], 'classes': ['collapse']}),
    ]

admin.site.register(Segment, SegmentAdmin)
