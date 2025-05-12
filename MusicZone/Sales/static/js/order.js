function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function updateStatus(selectElement) {
    const form = selectElement.closest('form');
    const url = form.dataset.url;
    const newStatus = selectElement.value;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ 'new_status': newStatus })
    })
    .then(response => {
        if (!response.ok) {
            alert("Hubo un error al actualizar el estado.");
        }
    });
}