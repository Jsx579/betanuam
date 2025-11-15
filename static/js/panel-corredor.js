// static/js/panel-corredor.js

/**
 * Funcionalidades específicas del panel del corredor
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Animar contadores
    animarContadores();
    
    // Filtros de tabla
    inicializarFiltros();
    
    // Búsqueda en tiempo real
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            filtrarTabla(this.value);
        });
    }
});

/**
 * Animar los números de los contadores
 */
function animarContadores() {
    const contadores = document.querySelectorAll('[data-contador]');
    
    contadores.forEach(contador => {
        const valorFinal = parseInt(contador.textContent);
        let valorActual = 0;
        const incremento = Math.ceil(valorFinal / 30);
        
        const intervalo = setInterval(() => {
            valorActual += incremento;
            if (valorActual >= valorFinal) {
                valorActual = valorFinal;
                clearInterval(intervalo);
            }
            contador.textContent = valorActual;
        }, 30);
    });
}

/**
 * Filtrar tabla por texto de búsqueda
 */
function filtrarTabla(texto) {
    const tabla = document.querySelector('table tbody');
    if (!tabla) return;
    
    const filas = tabla.querySelectorAll('tr');
    texto = texto.toLowerCase();
    
    filas.forEach(fila => {
        const contenido = fila.textContent.toLowerCase();
        if (contenido.includes(texto)) {
            fila.style.display = '';
        } else {
            fila.style.display = 'none';
        }
    });
}

/**
 * Inicializar filtros de estado y mercado
 */
function inicializarFiltros() {
    const filtroEstado = document.getElementById('filtroEstado');
    const filtroMercado = document.getElementById('filtroMercado');
    
    if (filtroEstado) {
        filtroEstado.addEventListener('change', aplicarFiltros);
    }
    
    if (filtroMercado) {
        filtroMercado.addEventListener('change', aplicarFiltros);
    }
}

/**
 * Aplicar filtros combinados
 */
function aplicarFiltros() {
    const filtroEstado = document.getElementById('filtroEstado')?.value || '';
    const filtroMercado = document.getElementById('filtroMercado')?.value || '';
    const tabla = document.querySelector('table tbody');
    
    if (!tabla) return;
    
    const filas = tabla.querySelectorAll('tr');
    
    filas.forEach(fila => {
        const estado = fila.querySelector('[data-estado]')?.dataset.estado || '';
        const mercado = fila.querySelector('[data-mercado]')?.dataset.mercado || '';
        
        let mostrar = true;
        
        if (filtroEstado && estado !== filtroEstado) {
            mostrar = false;
        }
        
        if (filtroMercado && mercado !== filtroMercado) {
            mostrar = false;
        }
        
        fila.style.display = mostrar ? '' : 'none';
    });
}
