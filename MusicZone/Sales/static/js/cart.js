document.getElementById("saleForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Obtener la URL de 'cart_view' desde el atributo data-url del botón
    const cartViewUrl = event.target.querySelector('button').getAttribute('data-url');

    fetch(this.action, {
        method: "POST",
        body: new FormData(this),
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Swal.fire({
                title: "¡Todo listo!",
                text: data.message,
                icon: "success",
                confirmButtonColor: "#6b8e23",
                confirmButtonText: "OK"
            }).then(() => {
                window.location.href = cartViewUrl;
            });
        } else {
            Swal.fire({
                title: "Error",
                text: data.message,
                icon: "error",
                confirmButtonColor: "#d33"
            });
        }
    })
    .catch(error => {
        console.error("Error:", error);
        Swal.fire({
            title: "Error",
            text: "Ocurrió un error al realizar el pedido.",
            icon: "error",
            confirmButtonColor: "#d33"
        });
    });
});