from django.contrib import admin

# Register your models here.
from .models import Submission

class MapSubmissionAdmin(admin.ModelAdmin):
    list_display = ('mapper_name','map_name','status','submitted_date')
    list_filter = ('status','submitted_date')
    search_fields = ('mapper_name','status','submitted_date')
    date_hierarchy = ('submitted_date')