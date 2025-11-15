from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
import pandas as pd
from datetime import datetime
from .models import Calificacion
from .forms import CalificacionForm


# ==================== PANELES POR ROL ====================


def index(request):
    if request.user.is_authenticated and hasattr(request.user, 'perfil'):
        rol = request.user.perfil.rol
        if rol == 'corredor':
            return redirect('nuam_app:panel_corredor')
        elif rol == 'auditor':
            return redirect('nuam_app:panel_auditor')
        elif rol == 'administrador':
            return redirect('nuam_app:panel_administrador')
    return render(request, 'nuam_app/index.html')


def panel_corredor(request):
    if not request.user.is_authenticated:
        estadisticas = {'total': 0, 'pendientes': 0, 'aprobadas': 0, 'rechazadas': 0}
        calificaciones_recientes = []
    else:
        user = request.user
        calificaciones = Calificacion.objects.filter(corredor=user)
        estadisticas = {
            'total': calificaciones.count(),
            'pendientes': calificaciones.filter(estado='pendiente').count(),
            'aprobadas': calificaciones.filter(estado='aprobado').count(),
            'rechazadas': calificaciones.filter(estado='rechazado').count(),
        }
        calificaciones_recientes = calificaciones.order_by('-fecha_ingreso')[:10]
    context = {
        'estadisticas': estadisticas,
        'calificaciones': calificaciones_recientes,
    }
    return render(request, 'nuam_app/panel_corredor.html', context)


def panel_auditor(request):
    pendientes = Calificacion.objects.filter(estado='pendiente')
    mercado = request.GET.get('mercado')
    if mercado:
        pendientes = pendientes.filter(mercado=mercado)
    paginator = Paginator(pendientes, 15)
    page = request.GET.get('page')
    calificaciones = paginator.get_page(page)
    context = {
        'calificaciones': calificaciones,
        'total_pendientes': pendientes.count(),
    }
    return render(request, 'nuam_app/panel_auditor.html', context)


def panel_administrador(request):
    estadisticas = {
        'total_calificaciones': Calificacion.objects.count(),
        'por_mercado': Calificacion.objects.values('mercado').annotate(total=Count('id')),
        'por_estado': Calificacion.objects.values('estado').annotate(total=Count('id')),
    }
    context = {'estadisticas': estadisticas}
    return render(request, 'nuam_app/panel_administrador.html', context)


def panel_reportes(request):
    return render(request, 'panel_reportes.html')


# ==================== GESTIÓN DE CALIFICACIONES ====================


def ingreso_calificacion(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para crear calificaciones.")
        return redirect('nuam_app:index')
