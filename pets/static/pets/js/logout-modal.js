document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('logout-modal');

    window.onclick = function (event) {
        if (event.target === modal) {
            closeModal()
        }
    }

    function openModal() {
        modal.style.display = "flex"
    }

    function closeModal() {
        modal.style.display = "none"
    }

    window.openModal = openModal;
    window.closeModal = closeModal;
})

