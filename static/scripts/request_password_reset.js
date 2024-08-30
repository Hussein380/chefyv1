document.addEventListener('DOMContentLoaded', function () {
    const requestPasswordForm = document.getElementById('request-password-form');

    requestPasswordForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const email = document.getElementById('email').value;

        fetch('/auth/request_password_reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        })
        .then(response => response.json())
        .then(data => {
            const messageDiv = document.getElementById('message');
            if (data.error) {
                messageDiv.textContent = data.error;
                messageDiv.style.color = 'red';
            } else {
                messageDiv.textContent = data.message;
                messageDiv.style.color = 'green';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = 'An error occurred. Please try again later.';
            messageDiv.style.color = 'red';
        });
    });
});

