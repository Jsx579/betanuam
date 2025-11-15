# nuam_app/urls.py
from django.urls import path
from . import views

app_name = 'nuam_app'

urlpatterns = [
    # Panel principal
    path('', views.index, name='index'),
    
    # Paneles por rol
    path('panel/corredor/', views.panel_corredor, name='panel_corredor'),
    path('panel/auditor/', views.panel_auditor, name='panel_auditor'),
    path('panel/admin/', views.panel_administrador, name='panel_administrador'),
    
    # Gestión de calificaciones
    path('ingreso/', views.ingreso_calificacion, name='ingreso_calificacion'),
    path('carga-masiva/', views.carga_masiva, name='carga_masiva'),
    path('editar/<int:pk>/', views.editar_calificacion, name='editar_calificacion'),
    path('eliminar/<int:pk>/', views.eliminar_calificacion, name='eliminar_calificacion'),
    
    # Revisión auditor
    path('revisar/<int:pk>/', views.revisar_calificacion, name='revisar_calificacion'),
    path('aprobar/<int:pk>/', views.aprobar_calificacion, name='aprobar_calificacion'),
    path('rechazar/<int:pk>/', views.rechazar_calificacion, name='rechazar_calificacion'),
    
    # Reportes
    path('reportes/', views.panel_reportes, name='panel_reportes'),
    path('reportes/descargar/<str:formato>/', views.descargar_reporte, name='descargar_reporte'),
]
