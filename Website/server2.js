const express = require('express'); // for building the network and handling http requests
const fs = require('fs'); // to read and write files (json database)
const cors = require('cors'); // to allow other domains to access the website
const app = express(); // Create an instance of Express


app.use(express.json()); // Middleware to read json files
app.use(express.static('public')); // Middleware to serve static (that do not change) files from the 'public' directory
app.use(cors()); // to make CORS work


const uuid = require('uuid'); // import a package to generate unique IDs


// Register endpoint
app.post('/register', (req, res) => {
    const userData = req.body; // we extract the data sent by the user and store it in a variable "userData"

    // Generate a unique ID for the user
    const userId = uuid.v4(); // This creates a unique ID for each user
    userData.id = userId; // Add the ID to the user data

    // Attempt to read and update users.json
    let users = [];
    try {
        if (fs.existsSync('users.json')) { // if users.json exists
            users = JSON.parse(fs.readFileSync('users.json', 'utf-8')); // all the existing users are stored in a variable named "users"
        }
    } catch (err) {
        console.error('Error reading users.json:', err); // if there is an error: error message
    }

    users.push(userData); // add the new user data to the users array


    // Write the updated user data back to users.json
    try {
        fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
        res.status(201).send({ message: 'User registered successfully!', userId }); // it sends back a success message + the userId to the user
    } catch (err) {
        console.error('Error writing to users.json:', err);
        res.status(500).send({ message: 'Error saving user data' });
    }
});

// Login endpoint
app.post('/login', (req, res) => {
    const loginData = req.body; // extract login details and stores them in loginData

    // Ensure email and password are provided and if not: stop the following code to run
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

    // Normalize loginData
    const email = loginData.email.trim().toLowerCase(); // remove extra space from the email + everything in lowercase
    const password = loginData.password.trim(); // remove any spaces

    // Find the user by email and password
    const user = users.find(user => (user.email.trim().toLowerCase() === email || user.phone === loginData.email) && user.password === password);

    if (user) {
        res.status(200).send({
            message: `Welcome, ${user.firstname}!`,
            userId: user.id,
            firstname: user.firstname
        }); // sends back the userId along with the firstname if an user is found
    } else {
        res.status(401).send({ message: 'Incorrect email or password' });
    }
});

// Subscription selection endpoint
app.post('/subscription', (req, res) => { // req = request and res = response
    const { plan } = req.body; // extract the chosen plan from the request body
    const userId = req.headers['user-id']; // extract the user ID from the request headers

    // Log received data for debugging
    console.log('Received Plan:', plan);
    console.log('Received User ID:', userId);

    // Validate input
    if (!plan || !['Basic', 'Standard', 'Premium'].includes(plan)) {
        console.error('Invalid subscription plan:', plan);
        return res.status(400).send({ success: false, message: 'Invalid subscription plan' });
    }
    if (!userId) {
        console.error('Missing User ID');
        return res.status(400).send({ success: false, message: 'User ID is missing' });
    }

    // Read the users database
    let users = [];
    try {
        if (fs.existsSync('users.json')) {
            users = JSON.parse(fs.readFileSync('users.json', 'utf-8'));
        }
    } catch (err) {
        console.error('Error reading users.json:', err);
        return res.status(500).send({ success: false, message: 'Error reading database' });
    }

    // Find the user by ID
    const user = users.find(u => u.id === userId);
    if (!user) {
        console.error('User not found for ID:', userId);
        return res.status(404).send({ success: false, message: 'User not found' });
    }

    // Update user's subscription
    user.subscription = plan;

    // Write the updated users database
    try {
        fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
        console.log('Subscription saved successfully for user:', userId);
        res.send({ success: true, message: 'Subscription saved successfully' });
    } catch (err) {
        console.error('Error writing to users.json:', err);
        res.status(500).send({ success: false, message: 'Error saving subscription data' });
    }
});

// Bank details endpoint
app.post('/bank', (req, res) => {
    const bankData = req.body;
    const userId = bankData.userId; // userId should come from bankData

    console.log('Received Bank Data:', bankData);

    // Validate user ID and bank data
    if (!userId) {
        return res.status(400).send({ message: 'User ID is missing' });
    }

    let users = [];
    try {
        if (fs.existsSync('users.json')) {
            users = JSON.parse(fs.readFileSync('users.json', 'utf-8'));
        }
    } catch (err) {
        console.error('Error reading users.json:', err);
        return res.status(500).send({ message: 'Error reading database' });
    }

    // Find the user by ID
    const user = users.find(u => u.id === userId);
    if (!user) {
        console.error('User not found:', userId);
        return res.status(404).send({ message: 'User not found' });
    }

    // Add bank details to the user's data
    user.bankDetails = bankData;

    try {
        // Save the updated user data with bank details
        fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
        res.send({ message: 'Bank details submitted successfully!' });
    } catch (err) {
        console.error('Error writing to users.json:', err);
        res.status(500).send({ message: 'Error saving bank details' });
    }
});


// **Add the /database endpoint here**
app.get('/database', (req, res) => {
    try {
        if (fs.existsSync('users.json')) {
            const data = fs.readFileSync('users.json', 'utf-8');
            res.json(JSON.parse(data)); // Send the parsed JSON data as response
        } else {
            res.status(404).send({ message: 'Database file not found' });
        }
    } catch (err) {
        console.error('Error reading users.json:', err);
        res.status(500).send({ message: 'Error reading database' });
    }
});


// Start the server and listen on port 3000
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on http://0.0.0.0:${PORT}`));
