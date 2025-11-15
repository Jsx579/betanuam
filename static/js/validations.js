// static/js/validations.js

/**
 * Validaciones globales para formularios NUAM
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Validar secuencia (debe ser > 10000)
    const secuenciaInputs = document.querySelectorAll('input[name="secuencia"]');
    secuenciaInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const valor = parseInt(this.value);
            if (valor <= 10000) {
                mostrarError(this, 'La secuencia debe ser mayor a 10000');
            } else {
                limpiarError(this);
            }
        });
    });
    
    // Validar mercado (solo ACN, RVI, RVE)
    const mercadoSelects = document.querySelectorAll('select[name="mercado"]');
    mercadoSelects.forEach(select => {
        select.addEventListener('change', function() {
            const valor = this.value;
            if (!['ACN', 'RVI', 'RVE'].includes(valor)) {
                mostrarError(this, 'Seleccione un mercado válido');
            } else {
                limpiarError(this);
            }
        });
    });
    
    // Validar factores (0-1)
    const factorInputs = document.querySelectorAll('input[name^="factor_"]');
    factorInputs.forEach(input => {
        input.addEventListener('input', function() {
            const valor = parseFloat(this.value);
            if (valor < 0 || valor > 1) {
                mostrarError(this, 'El factor debe estar entre 0 y 1');
            } else {
                limpiarError(this);
            }
        });
    });
    
    // Confirmación al eliminar
    const deleteButtons = document.querySelectorAll('[data-action="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de eliminar este registro?')) {
                e.preventDefault();
            }
        });
    });
});

/**
 * Mostrar mensaje de error en un campo
 */
function mostrarError(elemento, mensaje) {
    limpiarError(elemento);
    
    elemento.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = mensaje;
    errorDiv.id = `error-${elemento.name}`;
    
    elemento.parentNode.appendChild(errorDiv);
}

/**
 * Limpiar mensaje de error
 */
function limpiarError(elemento) {
    elemento.classList.remove('is-invalid');
    
    const errorDiv = document.getElementById(`error-${elemento.name}`);
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Mostrar toast de notificación
 */
function mostrarToast(mensaje, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${tipo} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}
