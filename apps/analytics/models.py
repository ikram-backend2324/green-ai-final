from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    REPORT_TYPES = [('daily','Daily'),('weekly','Weekly'),('monthly','Monthly'),('custom','Custom')]
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default='weekly')
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date_from = models.DateField()
    date_to = models.DateField()
    total_output_kwh = models.FloatField(default=0)
    total_co2_saved_kg = models.FloatField(default=0)
    avg_efficiency = models.FloatField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
