document.getElementById('proceed-button').addEventListener('click', () => {
    // Get the selected subscription plan
    const selectedPlan = document.querySelector('input[name="subscription"]:checked');

    // Check if a plan is selected
    if (!selectedPlan) {
        alert('Please select a subscription plan!');
        return;
    }

    // Get the value of the selected plan
    const plan = selectedPlan.value;

    // Retrieve the user ID from sessionStorage
    const userId = sessionStorage.getItem('userId'); // Make sure userId is stored after login

    if (!userId) {
        alert('User ID not found. Please log in again.');
        return;
    }

    // Send the plan to the server
    fetch('/subscription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'user-id': userId, // Send the correct user ID
        },
        body: JSON.stringify({ plan }),
    })
    .then(response => response.json())
    .then(data => {
        // Directly go to the bank page without alert
        if (data.success) {
            window.location.href = 'bank.html'; // Redirect to the bank page
        } else {
            alert(`Error saving subscription choice: ${data.message}`);
        }
    })
    .catch(error => console.error('Error:', error));
});
