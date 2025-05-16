$(document).ready(function () {
    const $form = $("#create-pet-form");

    $form.attr("method", "POST");

    $form.on("input", "input, select, textarea", function () {
        validateInput($(this));
    });

    // validate form on submit
    $form.on("submit", function (event) {
        let isValid = true;

        $form.find("input, select, textarea").each(function () {
            if (!validateInput($(this))) {
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
        } else {
            event.target.submit();
        }
    })

    // validate single input field
    function validateInput($input) {
        if (!$input || $input.length === 0) {
            console.warn("Warning: Invalid input element passed to validateInput()");
            return true; // Skip validation if input is missing
        }

        if ($input.closest("#vaccine-template").length > 0) {
            return true;
        }

        const val = $input.val()?.trim() || "";
        const inputId = $input.attr('id')
        const errorId = `${inputId}-error`
        const $error = $(`#${errorId}`);

        if (!$error.length) {
            console.warn(`No error element found for input ID: ${$input.attr("id")}`);
            return true;
        }

        const vetSelect = $("#vet-select");
        const selectedVet = vetSelect.val();
        const isCreatingNewVet = selectedVet === "";

        if (!isCreatingNewVet && inputId.startsWith("vet")) {
            return true;
        }

        $error.text("");
        $input.removeClass('input-error')

        const today = new Date();

        if (inputId === "pfp") {
            return true;
        }

        if (inputId === "petName") {
            if (val.length === 0) {
                $error.text("Please enter your pet's name.")
                $input.addClass("input-error");
                return false;
            } else if (val.length < 3) {
                $error.text("Pet's name must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Pet's name must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === "breed") {
            if (val.length === 0) {
                $error.text("Please enter your pet's breed.")
                $input.addClass("input-error");
                return false;
            }
            if (val.length < 3) {
                $error.text("Pet's breed must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Pet's breed must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === "dob") {
            const inputDate = new Date(val);
            if (inputDate > today) {
                $error.text("Please enter a date on or before today.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === "wgt") {
            if (isNaN(val) || val <= 0) {
                $error.text("Weight must be a positive, non-zero number.")
                $input.addClass("input-error");
                return false
            }
        } else if (inputId === "vetfname") {
            if (val.length === 0) {
                $error.text("Please enter your vet's first name.")
                $input.addClass("input-error");
                return false;
            } else if (val.length < 3) {
                $error.text("First name must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("First name must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === "vetlname") {
            if (val.length === 0) {
                $error.text("Please enter your vet's last name.")
                $input.addClass("input-error");
                return false;
            } else if (val.length < 3) {
                $error.text("Last name must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Last name must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (/\d/.test(val)) {
                $error.text("Last name may not contain any numbers.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === "vetPhone") {
            if (!/^(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$/.test(val)) {
                $error.text("Please enter a valid phone number.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === 'vetEmail') {
            if (val.length === 0) {
                $error.text("Please enter your vet's email address.")
                $input.addClass("input-error");
                return false
            } else if (!val.includes('@')) {
                $error.text("Please enter a valid email address")
                $input.addClass("input-error");
                return false
            } else if (val.length > 99) {
                $error.text("Email address must be less than 100 characters long.")
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === "vetClinic") {
            if (val.length === 0) {
                $error.text("Please enter your vet's clinic nane.")
                $input.addClass("input-error");
                return false
            } else if (val.length < 3) {
                $error.text("Clinic name must be at least 3 characters long.")
                $input.addClass("input-error");
                return false
            } else if (val.length > 100) {
                $error.text("Clinic name must be less than 100 characters long.")
                $input.addClass("input-error");
                return false
            }
        } else if (inputId === "vetAddress") {
            if (val.length === 0) {
                $error.text("Please enter the vet clinic street address.")
                $input.addClass("input-error");
                return false
            } else if (val.length < 3) {
                $error.text("Address must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Address must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (!(/\d/.test(val)) || !(/[a-zA-Z]/.test(val))) {
                $error.text("Address must contain at least 1 number and 1 letter.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === "vetCity") {
            if (val.length === 0) {
                $error.text("Please enter the vet clinic city.")
                $input.addClass("input-error");
                return false;
            } else if (val.length < 3) {
                $error.text("City must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("City must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId === "vetZip") {
            if (!/^\d{5}(-\d{4})?$/.test(val) || val.length === 0) {
                $error.text("Please enter a valid zip code.");
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId.includes("condition-title")) {
            if (val.length === 0) {
                $error.text("Please enter a condition title.")
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Title must be less than 30 characters long.")
                $input.addClass("input-error");
                return false
            }
        } else if (inputId.includes("condition-description")) {
            if (val.length === 0) {
                $error.text("Please enter a condition description.")
                $input.addClass("input-error");
                return false
            }
        } else if (inputId.includes("vac-name")) {
            if (val.length === 0) {
                $error.text("Please enter a vaccine name.")
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Name must be less than 30 characters long.")
                $input.addClass("input-error");
                return false;
            }
        } else if (inputId.includes("last-done")) {
            if (!val) {
                $error.text("Please enter a date on or before today.")
                $input.addClass("input-error");
                return false
            }
            const inputDate = new Date(val);
            if (inputDate > today) {
                $error.text("Please enter a date on or before today.")
                $input.addClass("input-error");
                return false
            }
        } else if (inputId.includes("next-due")) {
            if (!val) {
                return true;
            }
            const id = inputId.split("-").pop();
            const lastDone = $(`#last-done-${id}`);
            const lastDoneDate = new Date(lastDone.val())
            const nextDueDate = new Date(val)
            if (nextDueDate < lastDoneDate) {
                $error.text("Please enter a date after Last Done.")
                $input.addClass("input-error");
                return false;
            }
        }

        return true;
    }
})