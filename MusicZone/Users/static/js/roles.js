// Mostrar modal
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add("show");
}

// Ocultar modal
function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove("show");
}

// Modal de crear rol
function openCreateModal() {
    showModal("addRoleModal");
}

function closeCreateModal() {
    hideModal("addRoleModal");
}

// Modal de editar rol
function openEditModal(elemento) {
    const modal = document.getElementById("editRoleModal");

    const roleId = elemento.getAttribute("data-id");
    const roleName = elemento.getAttribute("data-name");

    document.getElementById("edit_role_id").value = roleId;
    document.getElementById("edit_role_name").value = roleName;

    const formEditar = document.getElementById("editForm");
    formEditar.action = `/usuarios/roles_edit/${roleId}/`;

    showModal("editRoleModal");
}

function closeEditModal() {
    hideModal("editRoleModal");
}

// Modal de eliminación
function openDeleteModal(roleId, roleName) {
    const form = document.getElementById('deleteForm');
    form.action = `/usuarios/roles_delete/${roleId}/`;
    document.getElementById('delete_role_name').textContent = `"${roleName}"`;

    showModal("deleteModal");
}

function closeDeleteModal() {
    hideModal("deleteModal");
}

// Cerrar el modal al hacer clic en el fondo negro
window.addEventListener("click", function (event) {
    const modals = document.querySelectorAll(".modal.show");

    modals.forEach(modal => {
        if (event.target === modal) {
            hideModal(modal.id);
        }
    });
});
