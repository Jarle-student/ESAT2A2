document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form submission

    // Clear previous errors
    document.getElementById('contactError').textContent = '';
    document.getElementById('passwordError').textContent = '';

    // Get form values
    const contact = document.getElementById('contact').value.trim();
    const password = document.getElementById('password').value.trim();

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

    // Validate password
    if (password.length < 8) { // Example of simple password check
        document.getElementById('passwordError').textContent = 'Password must be at least 8 characters long.';
        valid = false;
    }

    if (valid) {
        // Prepare the login data (contact can be either phone or email)
        const loginData = { email: contact, password: password };

        // Dynamically get the server's base URL
        const serverBaseUrl = window.location.origin;

        // Send login request to the server
        fetch(`${serverBaseUrl}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
        })
        .then(response => response.json())
        .then(data => {
            // Check if the response message indicates success
            if (data.firstname) { // Check if firstname is present in the response
                // Redirect to fout.html with the firstname query parameter
                window.location.href = `fout.html?firstname=${encodeURIComponent(data.firstname)}`;
            } else {
                // Display error message if login fails
                document.getElementById('contactError').textContent = 'Incorrect email or password.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error logging in');
        });
    } else {
        // Stay on the page and show errors if validation fails
        return false;
    }
});
