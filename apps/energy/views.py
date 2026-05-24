from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import EnergySource, EnergyReading


@login_required
def source_list(request):
    if request.user.is_staff:
        sources = EnergySource.objects.all().select_related('owner')
    else:
        sources = EnergySource.objects.filter(owner=request.user)
    context = {
        'sources': sources,
        'total_capacity': sum(s.capacity_kw for s in sources),
        'active_count': sources.filter(status='active').count(),
        'page_title': 'Energy Sources',
    }
    return render(request, 'energy/source_list.html', context)


@login_required
def source_detail(request, pk):
    source = get_object_or_404(EnergySource, pk=pk) if request.user.is_staff else get_object_or_404(EnergySource, pk=pk, owner=request.user)
    readings = source.readings.order_by('-timestamp')[:30]
    return render(request, 'energy/source_detail.html', {'source': source, 'readings': readings, 'page_title': source.name})


@login_required
def source_create(request):
    if request.method == 'POST':
        try:
            lat = request.POST.get('latitude')
            lng = request.POST.get('longitude')
            source = EnergySource.objects.create(
                name=request.POST['name'],
                source_type=request.POST['source_type'],
                capacity_kw=float(request.POST['capacity_kw']),
                location=request.POST['location'],
                status=request.POST.get('status', 'active'),
                installation_date=request.POST['installation_date'],
                owner=request.user,
                description=request.POST.get('description', ''),
                latitude=float(lat) if lat else None,
                longitude=float(lng) if lng else None,
            )
            messages.success(request, f'Energy source "{source.name}" created successfully.')
            return redirect('energy:source_detail', pk=source.pk)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'energy/source_form.html', {
        'source_types': EnergySource.SOURCE_TYPES,
        'status_choices': EnergySource.STATUS_CHOICES,
        'page_title': 'Add Energy Source',
    })


@login_required
def reading_create(request, source_pk):
    source = get_object_or_404(EnergySource, pk=source_pk) if request.user.is_staff else get_object_or_404(EnergySource, pk=source_pk, owner=request.user)
    if request.method == 'POST':
        try:
            EnergyReading.objects.create(
                source=source,
                timestamp=request.POST['timestamp'],
                output_kwh=float(request.POST['output_kwh']),
                efficiency_percent=float(request.POST.get('efficiency_percent', 0)),
                temperature_c=request.POST.get('temperature_c') or None,
                wind_speed_ms=request.POST.get('wind_speed_ms') or None,
                solar_irradiance=request.POST.get('solar_irradiance') or None,
                recorded_by=request.user,
            )
            messages.success(request, 'Reading added successfully.')
            return redirect('energy:source_detail', pk=source_pk)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'energy/reading_form.html', {
        'source': source,
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'page_title': f'Add Reading — {source.name}',
    })
