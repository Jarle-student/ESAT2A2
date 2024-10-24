// This document was partially created with the assistance of AI tools,
// including code generation from ChatGPT.

// Get references to the form and input fields
const form = document.getElementById('userForm');
const firstname = document.getElementById('firstname');
const email = document.getElementById('email');
const password = document.getElementById('password');
const password2 = document.getElementById('confirm');
const lastname = document.getElementById('lastname');
const phone = document.getElementById('phone');

// Add an event listener for form submission
form.addEventListener('submit', e => {
    e.preventDefault(); // Prevent the default form submission

    // Validate inputs before proceeding
    if (validateInputs()) {
        window.location.href = 'keuze.html'; // Redirect to keuze.html if all validations are successful
    }
});

// Function to display error messages
const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error'); // Add error class for styling
    inputControl.classList.remove('success');
};

// Function to indicate successful validation
const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success'); // Add success class for styling
    inputControl.classList.remove('error');
};

// Function to validate email format
const isValidEmail = email => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
};

// Function to validate all input fields
const validateInputs = () => {
    const firstnameValue = firstname.value.trim();
    const lastnameValue = lastname.value.trim();
    const phoneValue = phone.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const password2Value = password2.value.trim();

    let isValid = true; // For overall validity

    // Validate First Name
    if (firstnameValue === '') {
        setError(firstname, 'First Name is required');
        isValid = false;
    } else {
        setSuccess(firstname);
    }

    // Validate Last Name
    if (lastnameValue === '') {
        setError(lastname, 'Last Name is required');
        isValid = false;
    } else {
        setSuccess(lastname);
    }

    // Validate Phone Number
    const phonePattern = /^04\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d$/;
    if (phoneValue === '') {
        setError(phone, 'Phone number is required');
        isValid = false;
    } else if (!phonePattern.test(phoneValue)) {
        setError(phone, 'Phone number must be in the format 0470 12 34 56');
        isValid = false;
    } else {
        setSuccess(phone);
    }

    // Validate Email
    if (emailValue === '') {
        setError(email, 'Email is required');
        isValid = false;
    } else if (!isValidEmail(emailValue)) {
        setError(email, 'Provide a valid email address');
        isValid = false;
    } else {
        setSuccess(email);
    }

    // Validate Password
    if (passwordValue === '') {
        setError(password, 'Password is required');
        isValid = false;
    } else if (passwordValue.length < 8) {
        setError(password, 'Password must be at least 8 characters.');
        isValid = false;
    } else {
        setSuccess(password);
    }

    // Validate Confirm Password
    if (password2Value === '') {
        setError(password2, 'Please confirm your password');
        isValid = false;
    } else if (password2Value !== passwordValue) {
        setError(password2, "Passwords do not match");
        isValid = false;
    } else {
        setSuccess(password2);
    }

    return isValid; // Return overall validity status
};
