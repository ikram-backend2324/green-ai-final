from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.energy.models import EnergySource
from .models import OptimizationResult
from .ai_engine import run_optimization


@login_required
def optimization_list(request):
    if request.user.is_staff:
        results = OptimizationResult.objects.all().select_related('source', 'requested_by')
    else:
        results = OptimizationResult.objects.filter(requested_by=request.user).select_related('source')
    return render(request, 'optimization/list.html', {'results': results[:20]})


@login_required
def run_optimization_view(request, source_pk):
    if request.user.is_staff:
        source = get_object_or_404(EnergySource, pk=source_pk)
    else:
        source = get_object_or_404(EnergySource, pk=source_pk, owner=request.user)

    # Get language from session (set by JS via cookie or query param)
    language = request.GET.get('lang') or request.session.get('greenai_lang', 'en')

    readings = list(source.readings.order_by('-timestamp')[:30])
    result_obj = OptimizationResult.objects.create(
        source=source, requested_by=request.user, status='running'
    )
    try:
        ai_result = run_optimization(source, readings, language=language)
        result_obj.recommendation = ai_result['recommendation']
        result_obj.predicted_output_kwh = ai_result['predicted_output_kwh']
        result_obj.efficiency_score = ai_result['efficiency_score']
        result_obj.co2_saved_kg = ai_result['co2_saved_kg']
        result_obj.confidence = ai_result['confidence']
        result_obj.suggested_actions = ai_result['suggested_actions']
        result_obj.raw_data = ai_result
        result_obj.status = 'completed'
        result_obj.save()
        messages.success(request, 'Optimization completed successfully.')
    except Exception as e:
        result_obj.status = 'failed'
        result_obj.recommendation = str(e)
        result_obj.save()
        messages.error(request, f'Optimization failed: {str(e)}')

    return redirect('optimization:result_detail', pk=result_obj.pk)


@login_required
def result_detail(request, pk):
    if request.user.is_staff:
        result = get_object_or_404(OptimizationResult, pk=pk)
    else:
        result = get_object_or_404(OptimizationResult, pk=pk, requested_by=request.user)
    return render(request, 'optimization/result_detail.html', {'result': result})