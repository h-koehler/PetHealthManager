document.addEventListener("DOMContentLoaded", function() {
    const addConditionBtn = document.getElementById("add-condition");
    const conditionContainer = document.querySelector(".conditions");
    const conditionTemplate = document.getElementById("condition-template");

    let conditionCount = document.querySelectorAll(".form-textarea").length;

    addConditionBtn.addEventListener("click", function() {
        const clone = conditionTemplate.cloneNode(true);
        clone.style.display = "flex";
        clone.id = "";

        // update ids within clone
        clone.querySelector(".condition-title").name = `condition-title-${conditionCount}`;
        clone.getElementById("condition-title-error").name = `condition-title-error-${conditionCount}`
        clone.getElementById
    })

})