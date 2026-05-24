from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from apps.energy.models import EnergySource, EnergyReading
from apps.optimization.models import OptimizationResult
import json

@login_required
def analytics_dashboard(request):
    if request.user.is_staff:
        sources = EnergySource.objects.all()
        readings = EnergyReading.objects.all()
        optimizations = OptimizationResult.objects.filter(status='completed')
    else:
        sources = EnergySource.objects.filter(owner=request.user)
        source_ids = sources.values_list('id', flat=True)
        readings = EnergyReading.objects.filter(source_id__in=source_ids)
        optimizations = OptimizationResult.objects.filter(requested_by=request.user, status='completed')

    total_output = readings.aggregate(total=Sum('output_kwh'))['total'] or 0
    total_co2 = readings.aggregate(total=Sum('co2_saved_kg'))['total'] or 0
    avg_efficiency = readings.aggregate(avg=Avg('efficiency_percent'))['avg'] or 0
    avg_confidence = optimizations.aggregate(avg=Avg('confidence'))['avg'] or 0

    type_data = {}
    for source in sources:
        stype = source.get_source_type_display()
        source_output = source.readings.aggregate(total=Sum('output_kwh'))['total'] or 0
        type_data[stype] = type_data.get(stype, 0) + source_output

    recent_readings = readings.order_by('-timestamp')[:14]
    trend_labels = []
    trend_values = []
    for r in reversed(list(recent_readings)):
        trend_labels.append(r.timestamp.strftime('%m/%d %H:%M'))
        trend_values.append(round(r.output_kwh, 2))

    context = {
        'total_output': round(total_output, 2),
        'total_co2': round(total_co2, 2),
        'avg_efficiency': round(avg_efficiency, 1),
        'source_count': sources.count(),
        'optimization_count': optimizations.count(),
        'avg_confidence': round(avg_confidence * 100, 1),
        'type_labels': json.dumps(list(type_data.keys())),
        'type_values': json.dumps(list(type_data.values())),
        'trend_labels': json.dumps(trend_labels),
        'trend_values': json.dumps(trend_values),
        'recent_readings': recent_readings[:5],
    }
    return render(request, 'analytics/dashboard.html', context)
