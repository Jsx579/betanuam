# nuam_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Calificacion(models.Model):
    """Modelo para calificaciones tributarias"""
    
    MERCADO_CHOICES = [
        ('ACN', 'ACN - Acciones Nacionales'),
        ('RVI', 'RVI - Renta Variable Internacional'),
        ('RVE', 'RVE - Renta Variable Emergente'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    # Datos básicos
    corredor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='calificaciones_creadas'
    )
    secuencia = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(10001)]
    )
    razon_social = models.CharField(max_length=255)
    mercado = models.CharField(max_length=3, choices=MERCADO_CHOICES)
    tipo_sociedad = models.CharField(max_length=100)
    
    # Factores de calificación (8-19)
    factor_8 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_9 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_10 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_11 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_12 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_13 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_14 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_15 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_16 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_17 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_18 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    factor_19 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Auditoría
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente'
    )
    auditor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calificaciones_revisadas'
    )
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    comentarios_auditor = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha_ingreso']
        verbose_name = 'Calificación Tributaria'
        verbose_name_plural = 'Calificaciones Tributarias'
    
    def __str__(self):
        return f"{self.secuencia} - {self.razon_social}"
    
    @property
    def suma_factores(self):
        """Calcula la suma de factores 8-19"""
        return sum([
            float(getattr(self, f'factor_{i}', 0))
            for i in range(8, 20)
        ])
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.secuencia <= 10000:
            raise ValidationError({
                'secuencia': 'La secuencia debe ser mayor a 10000'
            })
        
        if self.mercado not in ['ACN', 'RVI', 'RVE']:
            raise ValidationError({
                'mercado': 'El mercado debe ser ACN, RVI o RVE'
            })
        
        suma = self.suma_factores
        if suma > 1.0:
            raise ValidationError({
                '__all__': f'La suma de factores es {suma:.4f}. Debe ser ≤ 1.0'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Perfil(models.Model):
    """Perfil de usuario con rol"""
    
    ROL_CHOICES = [
        ('corredor', 'Corredor'),
        ('auditor', 'Auditor'),
        ('administrador', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    telefono = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
