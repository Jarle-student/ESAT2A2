// Get the firstname from the URL query parameter
const urlParams = new URLSearchParams(window.location.search);
const firstname = urlParams.get('firstname');

// Select the message element
const messageElement = document.getElementById('message');

// Update the message based on the presence of the firstname parameter
if (firstname) {
    // Display a personalized message if firstname is found
    messageElement.textContent = `Congratulations, ${firstname}! You've successfully logged in.`;
} else {
    // Display a default message if no firstname is found
    messageElement.textContent = 'Congratulations, you have successfully logged in!';
}
