

// This document was partially created with the assistance of AI tools,
// including code generation from ChatGPT.


document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form submission

    // Clear previous errors
    document.getElementById('contactError').textContent = '';
    document.getElementById('passwordError').textContent = '';

    // Get form values
    const contact = document.getElementById('contact').value;
    const password = document.getElementById('password').value;

    // Regular expression for Belgian phone number (starts with 04 + 8 digits)
    const phonePattern = /^04\d{8}$/;
    // Regular expression for email validation
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    let valid = true;

    // Validate contact field (either phone or email)
    if (!phonePattern.test(contact) && !emailPattern.test(contact)) {
        document.getElementById('contactError').textContent = 'Please enter a valid phone number or email address.';
        valid = false;
    }

    // Validate password (optional: add your own password criteria)
    if (password.length < 8) { // Example of simple password check
        document.getElementById('passwordError').textContent = 'Password must be at least 8 characters long.';
        valid = false;
    }

    // Redirect to keuze.html if the form is valid, otherwise show error messages
    if (valid) {
        // Redirect to keuze.html
        window.location.href = 'fout.html';
    } else {
        // Display error messages in red (handled by error spans in the form)
        return false; // Stay on the page and show errors
    }
});
