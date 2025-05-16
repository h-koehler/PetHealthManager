document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('delete-modal');

    window.onclick = function (event) {
        if (event.target === modal) {
            closeDeleteModal()
        }
    }

    function openDeleteModal() {
        modal.style.display = "flex"
    }

    function closeDeleteModal() {
        modal.style.display = "none"
    }

    window.openDeleteModal = openDeleteModal;
    window.closeDeleteModal = closeDeleteModal;
})

