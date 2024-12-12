// retrieve form and input fields using HTML id
const form = document.getElementById('userForm');
const firstname = document.getElementById('firstname');
const email = document.getElementById('email');
const password = document.getElementById('password');
const password2 = document.getElementById('confirm');
const lastname = document.getElementById('lastname');
const phone = document.getElementById('phone');

const serverBaseUrl = window.location.origin; // Dynamically get the server's base URL

document.getElementById("phone").addEventListener("input", function (event) {
    // Allow only digits and limit to 10 characters
    this.value = this.value.replace(/\D/g, '').substring(0, 10);
});


form.addEventListener('submit', e => {
    e.preventDefault(); // add event listener and prevent default form submission

    if (validateInputs()) { // if all fields are filled and VALID
        const userData = {
            firstname: firstname.value.trim(),
            lastname: lastname.value.trim(),
            phone: phone.value.trim(),
            email: email.value.trim(),
            password: password.value.trim()
        };

        // Send a POST request to the server using the server URL
        fetch(`${serverBaseUrl}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // specifies that the data is in JSON format
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            // Handle server response
            console.log('Success:', data);
            if (data.message === 'User registered successfully!') {
                sessionStorage.setItem('userId', data.userId); // Store the user ID in sessionStorage
                window.location.href = 'keuze.html'; // Redirect to the next page
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Error registering user');
        });
    }
});

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');
    errorDisplay.innerText = message;

    // add CSS class for styling
    inputControl.classList.add('error');
    inputControl.classList.remove('success');
};

const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    // add CSS class for styling
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

const isValidEmail = email => {
    // pattern for used to match valid email formats
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase()); // converts the email to lowercase and checks if it matches the pattern
};

const validateInputs = () => {
    const firstnameValue = firstname.value.trim();
    const lastnameValue = lastname.value.trim();
    const phoneValue = phone.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const password2Value = password2.value.trim();

    let isValid = true; // Track overall validity

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
