document.addEventListener('DOMContentLoaded', function() {
    const shareButton = document.getElementById('share-button');
    const shareDropdownContainer = document.getElementById('share-dropdown-container');
    const shareDropdownForm = document.getElementById('share-form')
    shareButton.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent click from bubbling to the document
        if (shareDropdownContainer.style.display === 'none' || shareDropdownContainer.style.display === '') {
            shareDropdownContainer.style.display = 'block';
        } else {
            shareDropdownContainer.style.display = 'none';
        }
    });

    // Hide dropdown if clicking outside
    document.addEventListener('click', function(event) {
        if (!shareDropdownForm.contains(event.target)) {
            shareDropdownContainer.style.display = 'none';
        }
    });
});