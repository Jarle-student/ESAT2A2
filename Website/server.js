const express = require('express'); // Import Express
const fs = require('fs'); // Import File System
const cors = require('cors'); // Import CORS for cross-origin requests

const app = express(); // Create an instance of Express

// Middleware to parse JSON bodies
app.use(express.json());

// Middleware to serve static files from the 'public' directory
app.use(express.static('public'));

// Enable CORS for all origins
app.use(cors());

const uuid = require('uuid'); // Use a package like uuid to generate unique IDs

// Register endpoint
app.post('/register', (req, res) => {
    const userData = req.body;

    // Generate a unique ID for the user
    const userId = uuid.v4(); // This creates a unique ID for each user
    userData.id = userId; // Add the ID to the user data

    // Attempt to read and update users.json
    let users = [];
    try {
        if (fs.existsSync('users.json')) {
            users = JSON.parse(fs.readFileSync('users.json', 'utf-8'));
        }
    } catch (err) {
        console.error('Error reading users.json:', err);
    }

    // Push the new user data to the users array
    users.push(userData);

    // Write the updated user data back to users.json
    try {
        fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
        res.status(201).send({ message: 'User registered successfully!', userId }); // Send back the userId
    } catch (err) {
        console.error('Error writing to users.json:', err);
        res.status(500).send({ message: 'Error saving user data' });
    }
});

// Bank details endpoint
app.post('/bank', (req, res) => {
    const bankData = req.body;

    // Check if the userId exists in the bank data
    if (!bankData.userId) {
        return res.status(400).send({ message: 'User ID is missing' });
    }

    // Read the users data
    let users = [];
    try {
        if (fs.existsSync('users.json')) {
            users = JSON.parse(fs.readFileSync('users.json', 'utf-8'));
        }
    } catch (err) {
        console.error('Error reading users.json:', err);
        return res.status(500).send({ message: 'Error reading user data' });
    }

    // Find the user by ID and add the bank details
    const user = users.find(user => user.id === bankData.userId);
    if (user) {
        user.bankDetails = bankData; // Add bank details to the user object
        console.log('Updated user with bank details:', user);
    } else {
        console.error('User not found');
        return res.status(404).send({ message: 'User not found' });
    }

    // Write the updated users data back to users.json
    try {
        fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
        console.log('Bank details saved successfully!');
        res.status(201).send({ message: 'Bank details submitted successfully!' });
    } catch (err) {
        console.error('Error writing to users.json:', err);
        res.status(500).send({ message: 'Error saving bank details' });
    }
});

// Login endpoint
app.post('/login', (req, res) => {
    const loginData = req.body;

    if (!loginData.email || !loginData.password) {
        return res.status(400).send({ message: 'Email and password are required' });
    }

    // Read the users data
    let users = [];
    try {
        if (fs.existsSync('users.json')) {
            users = JSON.parse(fs.readFileSync('users.json', 'utf-8'));
        }
    } catch (err) {
        console.error('Error reading users.json:', err);
        return res.status(500).send({ message: 'Error reading user data' });
    }

    // Normalize loginData (trim whitespaces, convert to lowercase for email comparison)
    const email = loginData.email.trim().toLowerCase();
    const password = loginData.password.trim(); // Keep password as is, but trim any spaces

    // Find the user by email and password
    const user = users.find(user => user.email.trim().toLowerCase() === email && user.password === password);

    if (user) {
        res.status(200).send({ message: `Welcome, ${user.firstname}!`, firstname: user.firstname });
    } else {
        res.status(401).send({ message: 'Incorrect email or password' });
    }
});

// Congratulations route
app.get('/fout.html', (req, res) => {
    const { firstname } = req.query;
    if (!firstname) {
        return res.status(400).send({ message: 'Firstname is missing from the query' });
    }
    res.send(`
        <h1>Congratulations, ${firstname}!</h1>
        <p>You've successfully logged in.</p>
    `);
});

// Start the server and listen on port 3000
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on http://0.0.0.0:${PORT}`));
