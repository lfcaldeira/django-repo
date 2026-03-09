import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
# Register your models here.
from .models import Submission

@admin.action(description='Export selected rides to CSV')
def export_as_csv(modeladmin, request, queryset):
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f"mapsbora_rides_{today}.csv"
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    
    # Headers
    writer.writerow(['Map Name', 'Date', 'Status', 'Mapper', 'URL'])
    
    # Data
    for obj in queryset:
        writer.writerow([obj.map_name, 
                         obj.request_date, 
                         obj.status, 
                         obj.mapper_name, 
                         obj.map_url
                         ])
    
    return response

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('mapper_name','map_name','map_url','request_date', 'status', 'token')
    list_filter = ('status', 'request_date','map_url')
    search_fields = ('map_name', 'mapper_name','status','map_url')
    date_hierarchy = ('request_date')
    list_editable = ('status',)
    actions = [export_as_csv]

