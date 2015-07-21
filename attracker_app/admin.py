from django.contrib import admin

# Register your models here.

from .models import AppalachianTrail, Segment, Hiker

admin.site.register(AppalachianTrail)
admin.site.site_header = 'AT Tracker Admin'


class SegmentInline(admin.TabularInline):
    model = Segment
    extra = 0

class HikerAdmin(admin.ModelAdmin):
    list_display = ('trail_name', 'full_name', 'number_segments')
    search_fields = ['trail_name','user__last_name','user__first_name']
    fieldsets = [
        (None,               {'fields': ['trail_name', 'user']}),
    ]
    inlines = [SegmentInline]

admin.site.register(Hiker, HikerAdmin)
