from django.db import models
from django.contrib.auth.models import User


class EnergySource(models.Model):
    SOURCE_TYPES = [
        ('solar', 'Solar'), ('wind', 'Wind'), ('hydro', 'Hydro'),
        ('biomass', 'Biomass'), ('geothermal', 'Geothermal'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'), ('inactive', 'Inactive'), ('maintenance', 'Maintenance'),
    ]
    name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    capacity_kw = models.FloatField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    installation_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='energy_sources')
    description = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"

    class Meta:
        verbose_name = "Energy Source"
        verbose_name_plural = "Energy Sources"
        ordering = ['-created_at']


class EnergyReading(models.Model):
    source = models.ForeignKey(EnergySource, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField()
    output_kwh = models.FloatField()
    efficiency_percent = models.FloatField(default=0.0)
    temperature_c = models.FloatField(null=True, blank=True)
    wind_speed_ms = models.FloatField(null=True, blank=True)
    solar_irradiance = models.FloatField(null=True, blank=True)
    co2_saved_kg = models.FloatField(default=0.0)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.source.name} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        self.co2_saved_kg = self.output_kwh * 0.233
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Energy Reading"
        verbose_name_plural = "Energy Readings"
        ordering = ['-timestamp']
