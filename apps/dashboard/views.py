from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from apps.energy.models import EnergySource, EnergyReading
from apps.optimization.models import OptimizationResult

@login_required
def dashboard_index(request):
    if request.user.is_staff:
        sources = EnergySource.objects.all()
        readings = EnergyReading.objects.all()
        recent_optimizations = OptimizationResult.objects.filter(status='completed').order_by('-created_at')[:5]
    else:
        sources = EnergySource.objects.filter(owner=request.user)
        source_ids = sources.values_list('id', flat=True)
        readings = EnergyReading.objects.filter(source_id__in=source_ids)
        recent_optimizations = OptimizationResult.objects.filter(requested_by=request.user, status='completed').order_by('-created_at')[:5]

    total_output = readings.aggregate(total=Sum('output_kwh'))['total'] or 0
    total_co2 = readings.aggregate(total=Sum('co2_saved_kg'))['total'] or 0
    avg_efficiency = readings.aggregate(avg=Avg('efficiency_percent'))['avg'] or 0
    active_sources = sources.filter(status='active').count()

    context = {
        'total_output': round(total_output, 2),
        'total_co2': round(total_co2, 2),
        'avg_efficiency': round(avg_efficiency, 1),
        'active_sources': active_sources,
        'total_sources': sources.count(),
        'recent_optimizations': recent_optimizations,
        'recent_readings': readings.order_by('-timestamp')[:6],
        'sources': sources[:6],
    }
    return render(request, 'dashboard/index.html', context)
