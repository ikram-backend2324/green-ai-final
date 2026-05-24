from django.db import models
from django.contrib.auth.models import User
from apps.energy.models import EnergySource


class OptimizationResult(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('running', 'Running'),
        ('completed', 'Completed'), ('failed', 'Failed'),
    ]
    source = models.ForeignKey(EnergySource, on_delete=models.CASCADE, related_name='optimizations')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    recommendation = models.TextField(blank=True)
    predicted_output_kwh = models.FloatField(null=True, blank=True)
    efficiency_score = models.FloatField(null=True, blank=True)
    co2_saved_kg = models.FloatField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    suggested_actions = models.JSONField(default=list, blank=True)
    raw_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Optimization for {self.source.name} [{self.status}]"

    class Meta:
        verbose_name = "Optimization Result"
        verbose_name_plural = "Optimization Results"
        ordering = ['-created_at']
