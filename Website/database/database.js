// Fetch the database content from the server and display it in the table
fetch('/database')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not OK');
        }
        return response.json();
    })
    .then(data => {
        const tableBody = document.querySelector('#database-table tbody');
        tableBody.innerHTML = ''; // Clear table contents before adding rows

        // Define the column names that should be displayed
        const columnNames = [
            'Firstname', 'Lastname', 'Email', 'Phone', 'Subscription', 'Password', 'Bank Details'
        ];

        // Iterate over each user and display their full details, with column names
        data.forEach(user => {
            const row = document.createElement('tr');

            // Generate HTML for each column (replace key with column names)
            row.innerHTML = `
                <td>${user.firstname}</td>
                <td>${user.lastname}</td>
                <td>${user.email}</td>
                <td>${user.phone}</td>
                <td>${user.subscription}</td>
                <td>${user.password}</td>
                <td>
                    ${user.bankDetails ? `
                        <strong>Name:</strong> ${user.bankDetails.name}<br>
                        <strong>Card:</strong> ${user.bankDetails.card}<br>
                        <strong>Expiry Date:</strong> ${user.bankDetails.date}<br>
                        <strong>CVC Code:</strong> ${user.bankDetails.code}` : 'No bank details'}
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching database:', error);
        const tableBody = document.querySelector('#database-table tbody');
        tableBody.innerHTML = `<tr><td colspan="7">Error loading data</td></tr>`;
    });
