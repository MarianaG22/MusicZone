// Modal de crear rol
function openCreateModal() {
    document.getElementById('addRoleModal').style.display = 'block';
}

function closeCreateModal() {
    document.getElementById('addRoleModal').style.display = 'none';
}
// Modal de editar rol
function openEditModal(elemento) {
    const modal = document.getElementById("editRoleModal");

    // Obtener los datos desde el botón o elemento
    const roleId = elemento.getAttribute("data-id");
    const roleName = elemento.getAttribute("data-name");

    // Llenar los campos del modal
    document.getElementById("edit_role_id").value = roleId;
    document.getElementById("edit_role_name").value = roleName;

    // Actualizar la acción del formulario
    const formEditar = document.getElementById("editForm");
    formEditar.action = `/usuarios/roles_edit/${roleId}/`;

    // Mostrar modal
    modal.style.display = "block";
}

function closeEditModal() {
    document.getElementById("editRoleModal").style.display = "none";
}

// Modal de eliminación
function openDeleteModal(roleId, roleName) {
    const form = document.getElementById('deleteForm');
    form.action = `/usuarios/roles_delete/${roleId}/`; 
    document.getElementById('delete_role_name').textContent = `"${roleName}"`;
    document.getElementById('deleteModal').style.display = "block";
}

function closeDeleteModal() {
    // Ocultar modal cuando el usuario le de en cerrar
    document.getElementById('deleteModal').style.display = "none";
}
