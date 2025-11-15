# nuam_app/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def corredor_required(view_func):
    """Decorador para vistas que requieren rol corredor"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'perfil'):
            messages.error(request, 'No tienes un perfil asignado.')
            return redirect('login')
        
        if request.user.perfil.rol != 'corredor':
            messages.error(request, 'No tienes permisos para acceder.')
            return redirect('nuam_app:index')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def auditor_required(view_func):
    """Decorador para vistas que requieren rol auditor"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'perfil'):
            messages.error(request, 'No tienes un perfil asignado.')
            return redirect('login')
        
        if request.user.perfil.rol != 'auditor':
            messages.error(request, 'No tienes permisos para acceder.')
            return redirect('nuam_app:index')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorador para vistas que requieren rol administrador"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'perfil'):
            messages.error(request, 'No tienes un perfil asignado.')
            return redirect('login')
        
        if request.user.perfil.rol != 'administrador':
            messages.error(request, 'No tienes permisos para acceder.')
            return redirect('nuam_app:index')
        
        return view_func(request, *args, **kwargs)
    return wrapper
