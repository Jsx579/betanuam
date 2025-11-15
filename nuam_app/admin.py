# nuam_app/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Calificacion, Perfil

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = [
        'secuencia', 'razon_social', 'mercado', 
        'estado_badge', 'corredor', 'fecha_ingreso'
    ]
    list_filter = ['estado', 'mercado', 'fecha_ingreso']
    search_fields = ['secuencia', 'razon_social', 'corredor__username']
    readonly_fields = ['fecha_ingreso', 'suma_factores']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('secuencia', 'razon_social', 'mercado', 'tipo_sociedad', 'corredor')
        }),
        ('Factores de Calificación', {
            'fields': (
                ('factor_8', 'factor_9', 'factor_10', 'factor_11'),
                ('factor_12', 'factor_13', 'factor_14', 'factor_15'),
                ('factor_16', 'factor_17', 'factor_18', 'factor_19'),
                'suma_factores',
            )
        }),
        ('Auditoría', {
            'fields': (
                'estado', 'auditor', 'fecha_ingreso', 
                'fecha_revision', 'comentarios_auditor'
            )
        }),
    )
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': 'orange',
            'aprobado': 'green',
            'rechazado': 'red',
        }
        color = colors.get(obj.estado, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def suma_factores(self, obj):
        suma = obj.suma_factores
        color = 'green' if suma <= 1.0 else 'red'
        return format_html(
            '<strong style="color: {};">{:.4f}</strong>',
            color,
            suma
        )
    suma_factores.short_description = 'Suma Factores'


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'telefono']
    list_filter = ['rol']
    search_fields = ['user__username', 'user__email']
