from django.contrib import admin
import csv
from django.http import HttpResponse
# Register your models here.
from .models import Submission

@admin.action(description='Export selected rides to CSV')
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mapsbora_rides.csv"'
    writer = csv.writer(response)
    
    # Cabeçalhos
    writer.writerow(['Map Name', 'Date', 'Status', 'Mapper', 'URL'])
    
    # Dados
    for obj in queryset:
        writer.writerow([obj.map_name, obj.request_date, obj.status, obj.mapper_name, obj.map_url])
    
    return response


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('map_name', 'request_date', 'status', 'token','mapper_name','map_url')
    list_filter = ('status', 'request_date','map_url')
    search_fields = ('map_name', 'mapper_name','status','map_url')
    date_hierarchy = ('request_date')
    list_editable = ('status',)

admin.site.register(Submission, SubmissionAdmin)

