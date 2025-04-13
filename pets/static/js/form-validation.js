$(document).ready(function () {
    const $form = $("#create-pet-form");

    $form.attr("method", "POST");

    $form.on("input", "input, select, textarea", function () {
        validateInput($(this));
    });

    // validate form on submit
    $form.on("submit", function (event) {
        event.preventDefault();
        let isValid = true;

        $form.find("input, select, textarea").each(function () {
            if (!validateInput($(this))) {
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
        } else {
            this.submit();
            $("#form-submitted").removeClass("display-none");
        }
    })

    // validate single input field
    function validateInput($input) {
        if (!$input || $input.length === 0) {
            console.warn("Warning: Invalid input element passed to validateInput()");
            return true; // Skip validation if input is missing
        }

        if ($input.attr("id") === "pfp") {
            return true;
        }

        const errorId = `${$input.attr("id")}-error`;
        const $error = $(`#${errorId}`);

        if (!$error.length) {
            console.warn(`No error element found for input ID: ${$input.attr("id")}`);
            return true;
        }

        $error.text("");
        $input.removeClass("input-error");

        const val = $input.val()?.trim() || "";

        if (!val) {
            if ($input.attr("id").includes('vac-name')) {
                $error.text("Please enter the vaccine name.");
            } else if ($input.attr("id").includes('last-done') || $input.attr("id").includes("next-due")) {
                $error.text("Please enter a valid date.");
            } else {
                $error.text(`Please enter your ${$input.attr("name").replace("-", " ")}.`);
            }
            $input.addClass("input-error");
            return false;
        }

        if ($input.attr("id") === "petName") {
            if (val.length < 3) {
                $error.text("Your pet's name must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Your pet's name must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (/\d/.test(val)) {
                $error.text("Your pet's name may not contain any numbers.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id") === "breed") {
            if (val.length < 3) {
                $error.text("Your pet's breed must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Your pet's breed must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (/\d/.test(val)) {
                $error.text("Your pet's breed may not contain any numbers.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id") === "dob") {
            const inputDate = new Date(val);
            const today = new Date();
            if (inputDate > today) {
                $error.text("Please enter a date before today.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id") === "wgt") {
            if (isNaN(val) || val <= 0) {
                $error.text("Your pet's weight must be a positive, non-zero number.")
                $input.addClass("input-error");
                return false
            }
        } else if ($input.attr("id") === "vetfname") {
            if (val.length < 3) {
                $error.text("Your vet's first name must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Your vet's first name must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (/\d/.test(val)) {
                $error.text("Your vet's first name may not contain any numbers.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id") === "vetlname") {
            if (val.length < 3) {
                $error.text("Your vet's last name must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Your vet's last name must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (/\d/.test(val)) {
                $error.text("Your vet's last name may not contain any numbers.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id") === "vetAddress") {
            if (val.length < 3) {
                $error.text("Your vet's address must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Your vet's address must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (!(/\d/.test(val)) || !(/[a-zA-Z]/.test(val))) {
                $error.text("Your vet's address must contain at least 1 number and 1 letter.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id") === "vetCity") {
            if (val.length < 3) {
                $error.text("Your vet's city must be at least 3 characters long.");
                $input.addClass("input-error");
                return false;
            } else if (val.length > 29) {
                $error.text("Your vet's city must be less than 30 characters long.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id") === "vetZip") {
            if (!/^\d{5}(-\d{4})?$/.test(val)) {
                $error.text("Please enter a valid zip code.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id") === "vetPhone") {
            if (!/^(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$/.test(val)) {
                $error.text("Please enter a valid phone number.");
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id").includes("vac-name")) {
            if (val.length < 3) {
                $error.text("The vaccine name must be at least 3 characters long.");
                $input.addClass('input-error');
                return false;
            } else if (val.length > 29) {
                $error.text("The vaccine name must less than 30 characters long.");
                $input.addClass('input-error');
                return false;
            }
        } else if ($input.attr("id").includes("last")) {
            const inputDate = new Date(val);
            const today = new Date();
            if (inputDate > today) {
                $error.text(`Please enter a date on or before today.`);
                $input.addClass("input-error");
                return false;
            }
        } else if ($input.attr("id").includes("next")) {
            const inputDate = new Date(val);
            const today = new Date();
            if (inputDate <= today) {
                $error.text(`Please enter a date after today.`);
                $input.addClass("input-error");
                return false;
            }
        }

        return true;
    }
})