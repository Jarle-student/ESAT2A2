// JavaScript to navigate to another HTML page on button click
document.getElementById('button').addEventListener('click', function() {
    // Dynamically construct the URL for navigation
    const baseUrl = window.location.origin;
    window.location.href = `${baseUrl}/index.html`; // Replace with the desired page if different
});
