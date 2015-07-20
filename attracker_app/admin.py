from django.contrib import admin

# Register your models here.

from .models import AppalachianTrail, Segment, Hiker

admin.site.register(AppalachianTrail)


class SegmentInline(admin.TabularInline):
    model = Segment
    extra = 0

class HikerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['trail_name', 'user']}),
    ]
    inlines = [SegmentInline]

admin.site.register(Hiker, HikerAdmin)
