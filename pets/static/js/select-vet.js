$(document).ready(function() {
    function toggleVetFields() {
        const selectedVetId = $('#vet-select').val();
        if (selectedVetId && selectedVetId !== "") {
            // An existing vet is selected
            $('#new-vet-fields').hide();
        } else {
            // "Create New Vet" is selected
            $('#new-vet-fields').show();
        }
    }

    // Run immediately on page load
    toggleVetFields();

    // Run again when user changes selection
    $('#vet-select').on('change', toggleVetFields);
});
