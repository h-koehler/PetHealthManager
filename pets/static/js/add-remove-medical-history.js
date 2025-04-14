document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("button[id^='delete-condition-']").forEach(btn => {
        attachConditionDeleteHandler(btn);
    });

    document.querySelectorAll("button[id^='vac-delete-']").forEach(btn => {
        attachVaccineDeleteHandler(btn);
    });

    let conditionIndex = 2;
    let vaccineIndex = 2;

    function attachVaccineDeleteHandler(button) {
        button.addEventListener("click", function () {
            const id = button.id;
            const index = id.split("-").pop();

            const vaccinesContainer = document.querySelector(".vaccines");

            const elementsToRemove = vaccinesContainer.querySelectorAll(
                `[for$="-${index}"],` +
                `#vac-name-${index},` +
                `#vac-name-error-${index},` +
                `#last-done-${index},` +
                `#last-done-error-${index},` +
                `#next-due-${index},` +
                `#next-due-error-${index},` +
                `#vac-delete-${index},` +
                `.name-div-${index},` +
                `.last-div-${index},` +
                `.next-div-${index}`
            );


            elementsToRemove.forEach(el => el.remove());
        })
    }

    function attachConditionDeleteHandler(button) {
        button.addEventListener("click", function () {
            const id = button.id;
            const index = id.split("-").pop();
            const condition = document.querySelector(`.condition-${index}`)
            if (condition) {
                condition.remove();
            }
        })
    }

    // add condition
    document.getElementById("add-condition").addEventListener("click", function () {
        const template = document.getElementById("condition-template")
        const copy = template.cloneNode(true);
        copy.removeAttribute("id");
        copy.classList.add("form-textarea");
        copy.classList.add(`condition-${conditionIndex}`);

        const titleInput = copy.querySelector(".condition-title");
        const titleError = copy.querySelector("#condition-title-error")
        const deleteButton = copy.querySelector("#delete-condition")
        const descriptionInput = copy.querySelector(".condition-description");
        const descriptionError = copy.querySelector("#description-error")

        titleInput.setAttribute("name", `condition-title-${conditionIndex}`);
        titleInput.setAttribute("id", `condition-title-${conditionIndex}`)

        titleError.setAttribute("id", `condition-error-${conditionIndex}`)
        deleteButton.setAttribute("id", `delete-condition-${conditionIndex}`)
        deleteButton.setAttribute("type", "button");
        attachConditionDeleteHandler(deleteButton)
        descriptionInput.setAttribute("name", `condition-description-${conditionIndex}`);
        descriptionInput.setAttribute("id", `condition-description-${conditionIndex}`);

        descriptionError.setAttribute("id", `description-error-${conditionIndex}`)

        titleInput.value = ""
        descriptionInput.value = "";

        document.querySelector(".conditions").append(copy);
        conditionIndex++
    })

    // add vaccine
    document.getElementById("add-vaccine").addEventListener("click", function () {
        const template = document.getElementById("vaccine-template")
        const copy = template.cloneNode(true);
        copy.removeAttribute("id");

        const nameLabel = copy.querySelector(".name-label")
        const nameDiv = copy.querySelector(".name-input")
        const nameInput = copy.querySelector(".name-input input")
        const nameError = copy.querySelector(".name-input span")

        const lastLabel = copy.querySelector(".last-label")
        const lastDiv = copy.querySelector(".last-input")
        const lastInput = copy.querySelector(".last-input input")
        const lastError = copy.querySelector(".last-input span")

        const nextLabel = copy.querySelector(".next-label")
        const nextDiv = copy.querySelector(".next-input")
        const nextInput = copy.querySelector(".next-input input")
        const nextError = copy.querySelector(".next-input span")

        const deleteLabel = copy.querySelector(".vac-delete")
        const deleteButton = copy.querySelector("#vac-delete")

        nameLabel.setAttribute("for", `vac-name-${vaccineIndex}`)
        nameDiv.classList.remove("name-input")
        nameDiv.classList.add(`name-div-${vaccineIndex}`)
        nameInput.id = `vac-name-${vaccineIndex}`
        nameInput.name = `vac-name-${vaccineIndex}`

        nameError.id = `vac-name-error-${vaccineIndex}`

        lastLabel.setAttribute("for", `last-done-${vaccineIndex}`)
        lastDiv.classList.remove("last-input")
        lastDiv.classList.add(`last-div-${vaccineIndex}`)
        lastInput.id = `last-done-${vaccineIndex}`
        lastInput.name = `last-done-${vaccineIndex}`

        lastError.id = `last-done-error-${vaccineIndex}`

        nextLabel.setAttribute("for", `next-due-${vaccineIndex}`)
        nextDiv.classList.remove("next-input")
        nextDiv.classList.add(`next-div-${vaccineIndex}`)
        nextInput.id = `next-due-${vaccineIndex}`
        nextInput.id = `next-due-${vaccineIndex}`
        nextInput.name = `next-due-${vaccineIndex}`

        nextError.id = `next-due-error-${vaccineIndex}`

        deleteLabel.setAttribute("for", `vac-delete-${vaccineIndex}`)
        deleteButton.id = `vac-delete-${vaccineIndex}`
        deleteButton.setAttribute("type", "button");
        attachVaccineDeleteHandler(deleteButton)


        Array.from(copy.children).forEach(child => document.querySelector(".vaccines").appendChild(child));
        vaccineIndex++
    })
})