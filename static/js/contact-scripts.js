function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === 'csrftoken') {
            return value;
        }
    }
    return null;
}

document.getElementById('contact-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    console.log('Form submitted'); // Debugging log

    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');
    const responseMessage = document.getElementById('response-message');

    const name = nameInput.value;
    const email = emailInput.value;
    const message = messageInput.value;

    console.log('Form values:', { name, email, message }); // Debugging log

    try {
        const response = await fetch('http://127.0.0.1:8000/api/contact/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), // CSRF token included here
            },
            body: JSON.stringify({ name, email, message }),
        });

        console.log('Fetch response:', response); // Debugging log

        const result = await response.json();
        console.log('Fetch result:', result); // Debugging log

        responseMessage.textContent = ''; // Clear previous messages

        if (response.ok) {
            console.log('Success! Clearing fields...');
            const successMessage = document.createElement('div');
            successMessage.className = 'alert alert-success';
            successMessage.textContent = result.success;
            responseMessage.appendChild(successMessage);

            // Clear the form fields
            nameInput.value = '';
            emailInput.value = '';
            messageInput.value = '';
        } else {
            console.log('Validation errors:', result);
            const errorMessage = document.createElement('div');
            errorMessage.className = 'alert alert-danger';

            if (result && typeof result === 'object') {
                errorMessage.innerHTML = Object.entries(result)
                    .map(([field, messages]) => `<strong>${field}:</strong> ${messages.join(', ')}`)
                    .join('<br>');
            } else {
                errorMessage.textContent = 'An error occurred. Please check your input.';
            }

            responseMessage.appendChild(errorMessage);
        }
    } catch (error) {
        console.error('Error:', error);
        responseMessage.textContent = ''; // Clear previous messages
        const errorMessage = document.createElement('div');
        errorMessage.className = 'alert alert-danger';
        errorMessage.textContent = 'An error occurred. Please try again.';
        responseMessage.appendChild(errorMessage);
    }
});
