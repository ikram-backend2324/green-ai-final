from django.contrib import admin
from .models import EnergySource, EnergyReading

@admin.register(EnergySource)
class EnergySourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'capacity_kw', 'location', 'status', 'owner', 'installation_date']
    list_filter = ['source_type', 'status']
    search_fields = ['name', 'location', 'owner__username']

@admin.register(EnergyReading)
class EnergyReadingAdmin(admin.ModelAdmin):
    list_display = ['source', 'timestamp', 'output_kwh', 'efficiency_percent', 'co2_saved_kg']
    list_filter = ['source__source_type']
    search_fields = ['source__name']
