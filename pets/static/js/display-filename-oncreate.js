document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById('pfp');
    const fileNameDisplay = document.getElementById('pfp-filename');

fileInput.addEventListener('change', function () {
    const file = fileInput.files[0]
    fileNameDisplay.textContent = file ? file.name : "No file selected"
})
})

