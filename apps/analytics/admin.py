from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'generated_by', 'date_from', 'date_to', 'total_output_kwh', 'created_at']
    list_filter = ['report_type']
    search_fields = ['title']
