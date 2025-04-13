document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('delete-modal');

    window.onclick = function (event) {
        if (event.target === modal) {
            closeDeleteModal()
        }
    }

    function openDeleteModal() {
        modal.style.display = "flex"
        // document.body.classList.add('no-scroll')
    }

    function closeDeleteModal() {
        modal.style.display = "none"
        // document.body.classList.remove('no-scroll')
    }

    window.openDeleteModal = openDeleteModal;
    window.closeDeleteModal = closeDeleteModal;
})

