// Formatear campos de precio al estilo ($ 1.000.000)
function formatCurrencyInput(input) {
    // Eliminar todo menos dígitos
    let value = input.value.replace(/[^\d]/g, '');
    if (value === '') {
        input.value = '';
        return;
    }

    // Formatear con separadores de miles y agregar símbolo $
    let formatted = new Intl.NumberFormat('es-CO').format(parseInt(value));
    input.value = `$ ${formatted}`;
}

function stripCurrency(inputId) {
    // Quitar formato antes de enviar el formulario
    let input = document.getElementById(inputId);
    let cleanValue = input.value.replace(/[^\d]/g, '');
    input.value = cleanValue;
}

// Eventos
document.getElementById('minPrice').addEventListener('input', function () {
    formatCurrencyInput(this);
});
document.getElementById('maxPrice').addEventListener('input', function () {
    formatCurrencyInput(this);
});

// Quitar formato antes de enviar
document.querySelector('form').addEventListener('submit', function () {
    stripCurrency('minPrice');
    stripCurrency('maxPrice');
});