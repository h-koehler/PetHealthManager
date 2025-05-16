$(document).ready(function () {
    const $form = $("#create-user-form");
    const role = $("#role").val();
    $form.attr('method', 'POST');

    $('#register-password').on('input', function () {
        validatePassword($(this))
    })

    $form.on('input', 'input, select', function () {
        validateInput($(this));
    });

    $form.on('submit', function (event) {
        console.log('Submit handler called');

        let isValid = true;

        $form.find('input, select').each(function () {
            if (!validateInput($(this))) {
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
        } else {
            event.target.submit();
        }
    });

    function validateInput($input) {
        if (!$input || $input.length === 0) {
            console.warn("Warning: Invalid input element passed to validtionInput()");
        }

        const inputId = $input.attr('id')
        const errorId = `${$input.attr('id')}-error`;
        const $error = $(`#${errorId}`);

        if (!$error.length) {
            console.warn(`No error element found for inputId: ${$input.attr('id')}`);
            return true;
        }

        $error.text('');

        const val = $input.val()?.trim() || '';

        if (inputId.includes('fname')) {
            if (val.length < 3) {
                $error.text('Your first name must be at least 3 characters long.')
                return false;
            } else if (val.length > 149) {
                $error.text('Your first name must be less than 150 characters long.')
                return false
            } else if (/\d/.test(val)) {
                $error.text("Your first name may not contain any numbers.");
                return false;
            }
        } else if (inputId.includes('lname')) {
            if (val.length < 3) {
                $error.text('Your last name must be at least 3 characters long.')
                return false;
            } else if (val.length > 149) {
                $error.text('Your last name must be less than 150 characters long.')
                return false
            } else if (/\d/.test(val)) {
                $error.text("Your last name may not contain any numbers.");
                return false;
            }
        } else if (inputId.includes('phone')) {
            if (!/^(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$/.test(val)) {
                $error.text("Please enter a valid phone number.");
                return false;
            }
        } else if (inputId.includes('email')) {
            if (!val.includes('@')) {
                $error.text('Please enter a valid email address.');
                return false;
            }
        } else if (inputId.includes('clinic')) {
            if (val.length < 3) {
                $error.text('Your clinic name must be at least 3 characters long.');
                return false;
            } else if (val.length > 149) {
                $error.text('Your clinic name must be less than 150 characters long.')
                return false
            }
        } else if (inputId.includes('address')) {
            console.log('role', role)
            if (val.length === 0 && role === 'o') {
                return true;
            } else if (val.length < 3) {
                $error.text("Your address must be at least 3 characters long.");
                return false;
            } else if (val.length > 149) {
                $error.text("Your address must be less than 150 characters long.");
                return false;
            } else if (!(/\d/.test(val)) || !(/[a-zA-Z]/.test(val))) {
                $error.text("Your address must contain at least 1 number and 1 letter.");
                return false;
            }
        } else if (inputId.includes('city')) {
            if (val.length === 0  && role === 'o') {
                return true;
            } else if (val.length < 3) {
                $error.text("Your city must be at least 3 characters long.");
                return false;
            } else if (val.length > 29) {
                $error.text("Your vet's city must be less than 30 characters long.");
                return false;
            }
        } else if (inputId.includes('state')) {
            if (val === 'Select') {
                $error.text("Please select a state or territory.");
                return false;
            }
        } else if (inputId.includes("zip")) {
            if (val.length === 0  && role === 'o') {
                return true;
            } else if (!/^\d{5}(-\d{4})?$/.test(val)) {
                $error.text("Please enter a valid zip code.");
                return false;
            }
        } else if (inputId === "register-password") {
            return validatePassword($input)
        } else if (inputId === "confirm-password") {
            if (val !== document.getElementById('register-password').value) {
                $error.text("Passwords do not match.");
                return false;
            }
        }

        return true;
    }

    function validatePassword($input) {

        const val = $input.val() || '';
        const passwordMessageItems = document.getElementsByClassName('password-message-item');

        let hasLower = /[a-z]/.test(val);
        let hasUpper = /[A-Z]/.test(val);
        let hasNumber = /[0-9]/.test(val);
        let hasSpecial = /[^A-Za-z0-9]/.test(val);
        let hasLength = val.length >= 8;

        passwordMessageItems[0].classList.toggle("valid", hasLower);
        passwordMessageItems[0].classList.toggle("invalid", !hasLower);

        passwordMessageItems[1].classList.toggle("valid", hasUpper);
        passwordMessageItems[1].classList.toggle("invalid", !hasUpper);

        passwordMessageItems[2].classList.toggle("valid", hasNumber);
        passwordMessageItems[2].classList.toggle("invalid", !hasNumber);

        passwordMessageItems[3].classList.toggle("valid", hasSpecial);
        passwordMessageItems[3].classList.toggle("invalid", !hasSpecial);

        passwordMessageItems[4].classList.toggle("valid", hasLength);
        passwordMessageItems[4].classList.toggle("invalid", !hasLength);

        return hasLower && hasUpper && hasNumber && hasSpecial && hasLength;
    }

})