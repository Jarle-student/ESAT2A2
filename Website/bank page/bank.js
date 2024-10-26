
// This document was partially created with the assistance of AI tools,
// including code generation from ChatGPT.



document.getElementById("card").addEventListener("input", function(event) {
    let cardNumber = event.target.value.replace(/\s+/g, ''); // Remove all spaces
    if (cardNumber.length > 0) {
        event.target.value = cardNumber.match(/.{1,4}/g).join(' '); // Insert space every 4 digits
    }
});

document.getElementById("date").addEventListener("input", function(event) {
    let input = event.target.value;
    // Remove any non-digit or non-slash characters
    input = input.replace(/[^\d\/]/g, '');

    // Automatically insert '/' after entering two digits for the month
    if (input.length === 2 && !input.includes('/')) {
        event.target.value = input + '/';
    } else {
        event.target.value = input;
    }
});

document.getElementById("checkoutForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission initially

    // Get form values
    const name = document.getElementById("name").value.trim();
    const code = document.getElementById("code").value.trim(); // CVC code
    const card = document.getElementById("card").value.replace(/\s+/g, ''); // Remove spaces for validation
    const date = document.getElementById("date").value.trim(); // Expiry date (MM/YY)

    // Clear previous error messages
    document.getElementById("nameError").textContent = '';
    document.getElementById("cardError").textContent = '';
    document.getElementById("dateError").textContent = '';
    document.getElementById("codeError").textContent = '';

    // Regular expressions
    const cardPattern = /^\d{16}$/; // 16 digits for card number
    const cvcPattern = /^\d{3,4}$/; // 3 or 4 digits for CVC code
    const datePattern = /^(0[1-9]|1[0-2])\/\d{2}$/; // Format MM/YY

    let valid = true;

    // Validate cardholder name
    if (!name) {
        valid = false;
        document.getElementById("nameError").textContent = 'Please enter the cardholder name.';
    }

    // Validate card number
    if (!cardPattern.test(card)) {
        valid = false;
        document.getElementById("cardError").textContent = 'Please enter a valid 16-digit card number.';
    }

    // Validate expiry date
    if (!datePattern.test(date)) {
        valid = false;
        document.getElementById("dateError").textContent = 'Please enter a valid expiry date (MM/YY).';
    }

    // Validate CVC code
    if (!cvcPattern.test(code)) {
        valid = false;
        document.getElementById("codeError").textContent = 'Please enter a valid 3- or 4-digit CVC code.';
    }

    // If valid, redirect to fout.html
    if (valid) {
        window.location.href = 'fout.html';
    }
});
