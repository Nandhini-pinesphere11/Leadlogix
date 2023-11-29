document.addEventListener("DOMContentLoaded", function() {
    // Get form fields
    const firstNameInput = document.getElementById("firstname");
    const lastNameInput = document.getElementById("lastname");
    const emailInput = document.getElementById("email");
    const messageInput = document.querySelector('textarea[name="message"]');
    const phoneInput = document.getElementById("phone");

    // Get error messages
    const firstNameError = document.getElementById("firstnameError");
    const lastNameError = document.getElementById("lastnameError");
    const emailError = document.getElementById("emailError");
    const messageError = document.getElementById("messageError");
    const phoneError = document.getElementById("phoneError");

    // Event listeners for input fields
    firstNameInput.addEventListener("blur", validateFirstName);
    lastNameInput.addEventListener("blur", validateLastName);
    emailInput.addEventListener("blur", validateEmail);
    messageInput.addEventListener("blur", validateMessage);
    phoneInput.addEventListener("blur", validatePhone);

    function validateFirstName() {
        if (firstNameInput.value.trim() === "") {
            firstNameInput.classList.add("invalid");
            firstNameError.style.display = "block";
        } else {
            firstNameInput.classList.remove("invalid");
            firstNameError.style.display = "none";
        }
    }

    function validateLastName() {
        // Similar logic as above for last name
        if (lastNameInput.value.trim() === "") {
            lastNameInput.classList.add("invalid");
            firstNameError.style.display = "block";
        } else {
            lastNameInput.classList.remove("invalid");
            lastNameError.style.display = "none";
        }
    }

    // Similar functions for email, message, and phone validation

    // Form submission
    const EnquiryForm = document.getElementById("EnquiryForm");
    EnquiryForm.addEventListener("submit", function(e) {
        e.preventDefault();

        validateFirstName();
        validateLastName();
        validateEmail();
        validateMessage();
        validatePhone();

        // If all validations pass, submit the form
        if (!EnquiryForm.querySelectorAll(".invalid").length) {
            EnquiryForm.submit();
        }
    });
});
