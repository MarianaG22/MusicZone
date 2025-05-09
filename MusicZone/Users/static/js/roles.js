document.addEventListener('DOMContentLoaded', function () {
    const createModal = document.getElementById('addRoleModal');
    const editModal = document.getElementById('editRoleModal');
    const deleteModal = document.getElementById('deleteRoleModal');
    const rolesModalElement = document.getElementById('rolesModal');
    const rolesModalInstance = bootstrap.Modal.getInstance(rolesModalElement) || new bootstrap.Modal(rolesModalElement);

    let nextModal = null;

    // Preparar datos para el modal de edición
    editModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const roleId = button.getAttribute('data-role-id');
        const roleName = button.getAttribute('data-role-name');

        document.getElementById('edit_role_id').value = roleId;
        document.getElementById('edit_role_name').value = roleName;
    });

    // Preparar datos para el modal de eliminación
    deleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const roleId = button.getAttribute('data-role-id');
        const roleName = button.getAttribute('data-role-name');

        document.getElementById('delete_role_name').textContent = roleName;
        document.getElementById('deleteRoleForm').action = `/usuarios/roles/delete/${roleId}/`;
    });

    // Detectar clic en botones de editar o eliminar
    document.querySelectorAll('[data-bs-target="#editRoleModal"], [data-bs-target="#deleteRoleModal"]').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = button.getAttribute('data-bs-target');
            nextModal = new bootstrap.Modal(document.querySelector(targetId));

            rolesModalInstance.hide(); // Oculta modal de roles pero no elimina el backdrop
        });
    });

    // Al cerrarse rolesModal, mostrar el modal siguiente (edit o delete)
    rolesModalElement.addEventListener('hidden.bs.modal', function () {
        if (nextModal) {
            nextModal.show();
            nextModal = null;
        } else {
            // Solo eliminar el fondo oscuro cuando se cierra completamente rolesModal
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.parentNode.removeChild(backdrop);
            }
        }
    });

    // Cuando se cierre editModal o deleteModal, volver a mostrar rolesModal
    [editModal, deleteModal, createModal].forEach(modal => {
        modal.addEventListener('hidden.bs.modal', function () {
            rolesModalInstance.show();
        });
    });

    // Mostrar el modal de roles cuando se cierre el modal de crear rol
    createModal.addEventListener('hidden.bs.modal', function () {
        rolesModalInstance.show(); // Muestra rolesModal cuando el modal de crear rol se cierra
    });
});
