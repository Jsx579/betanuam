# nuam_app/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    """Formulario para crear/editar calificaciones"""
    
    class Meta:
        model = Calificacion
        fields = [
            'secuencia', 'razon_social', 'mercado', 'tipo_sociedad',
            'factor_8', 'factor_9', 'factor_10', 'factor_11',
            'factor_12', 'factor_13', 'factor_14', 'factor_15',
            'factor_16', 'factor_17', 'factor_18', 'factor_19',
        ]
        widgets = {
            'secuencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mayor a 10000',
                'min': '10001'
            }),
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese razón social'
            }),
            'mercado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo_sociedad': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for i in range(8, 20):
            field_name = f'factor_{i}'
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'step': '0.0001',
                'min': '0',
                'max': '1'
            })
    
    def clean_secuencia(self):
        secuencia = self.cleaned_data.get('secuencia')
        if secuencia <= 10000:
            raise ValidationError('La secuencia debe ser mayor a 10000')
        return secuencia
    
    def clean_mercado(self):
        mercado = self.cleaned_data.get('mercado')
        if mercado not in ['ACN', 'RVI', 'RVE']:
            raise ValidationError('El mercado debe ser ACN, RVI o RVE')
        return mercado
    
    def clean(self):
        cleaned_data = super().clean()
        
        suma = sum([
            float(cleaned_data.get(f'factor_{i}', 0))
            for i in range(8, 20)
        ])
        
        if suma > 1.0:
            raise ValidationError(
                f'La suma de factores es {suma:.4f}. Debe ser ≤ 1.0'
            )
        
        return cleaned_data
