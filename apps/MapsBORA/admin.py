from django.contrib import admin

# Register your models here.
from .models import Submission

class MapSubmissionAdmin(admin.ModelAdmin):
    list_display = ('mapper_name','map_name','status','request_date')
    list_filter = ('status','request_date')
    search_fields = ('mapper_name','status','request_date')
    date_hierarchy = ('request_date')