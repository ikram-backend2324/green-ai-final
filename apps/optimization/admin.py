from django.contrib import admin
from .models import OptimizationResult

@admin.register(OptimizationResult)
class OptimizationResultAdmin(admin.ModelAdmin):
    list_display = ['source', 'requested_by', 'status', 'efficiency_score', 'predicted_output_kwh', 'confidence', 'created_at']
    list_filter = ['status', 'source__source_type']
    search_fields = ['source__name', 'requested_by__username']
    readonly_fields = ['raw_data', 'created_at']
