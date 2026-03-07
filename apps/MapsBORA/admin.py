from django.contrib import admin


# Register your models here.
from .models import Submission


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('map_name', 'request_date', 'status', 'token','mapper_name')
    list_filter = ('status', 'request_date')
    search_fields = ('map_name', 'mapper_name','status')
    date_hierarchy = ('request_date')
    list_editable = ('status',)

admin.site.register(Submission, SubmissionAdmin)