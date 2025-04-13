$(document).ready(function () {
    const $addVaccineBtn = $('#add-vaccine');
    const $vaccineContainer = $('.vaccines');
    const $numVacEntries = $('#num-vac-entries');

    let vaccineCount = $(".vaccines input[type='text']").length;

    function updateVaccineCount() {
        const totalVaccines = $(".vaccines input[type='text']").length;
        $numVacEntries.text(totalVaccines);
    }

    function getVaccineCount() {
        return $(".vaccines input[type='text']").length;
    }

    function setVaccineCountZero() {
        $numVacEntries.text(0);
    }

    function addDeleteEvent($deleteBtn, removeElements) {
    // check removeElements is an array
    if (!Array.isArray(removeElements)) {
        removeElements = [removeElements];
    }

    $deleteBtn.on("click", function () {
        if (getVaccineCount() === 1) {
            $vaccineContainer.addClass('hidden');
            setVaccineCountZero();
            return;
        }

        removeElements.forEach(element => {
            const $element = $(element);
            if (!$element.hasClass("vacc-header")) {
                $element.remove();
            }
        });

        $deleteBtn.remove();
        updateVaccineCount();
    });
}


    const $originalDeleteBtn = $(".vaccines i");
    addDeleteEvent($originalDeleteBtn, $vaccineContainer.children().toArray());

    $addVaccineBtn.on("click", function () {
        if ($numVacEntries.text() == 0) {
            $vaccineContainer.removeClass('hidden');
            updateVaccineCount();
            return;
        }

        $(".vaccines").removeClass('hidden');

        const $labels = $vaccineContainer.find("label");
        const $formInputContainers = $vaccineContainer.find(".form-input");

        vaccineCount++;

        // get vaccine row
        const clonedElements = [];
        for (let i = 0; i < 3; i++) {
            const $label = $labels.eq(-3 + i).clone();
            const $newFormInput = $formInputContainers.eq(-3 + i).clone();

            const $input = $newFormInput.find("input");
            const $errorSpan = $newFormInput.find(".error-message");

            // generate id
            const baseId = $input.attr("id").split("-").slice(0, 2).join("-");
            const newId = baseId + `-${vaccineCount}`;

            $input.attr({ id: newId, name: newId }).val("").removeClass('input-error');
            $label.attr("for", newId);
            $errorSpan.attr("id", newId + "-error").text("");

            clonedElements.push($label, $newFormInput);
        }

        // create delete button
        const $deleteBtn = $("<i>", { class: "fa-solid fa-trash-can delete-vaccine", css: { cursor: "pointer" } });

        addDeleteEvent($deleteBtn, clonedElements);

        // add new vaccine entry row
        clonedElements.forEach($inputDiv => $inputDiv.appendTo($vaccineContainer));
        $vaccineContainer.append($deleteBtn);
        updateVaccineCount();
    });

    updateVaccineCount();
});
