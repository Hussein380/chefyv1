document.getElementById('reset-password-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const newPassword = document.getElementById('new_password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const token = document.getElementById('token').value;  // Retrieve token from hidden field

    if (newPassword !== confirmPassword) {
        document.getElementById('message').textContent = "Passwords do not match.";
        document.getElementById('message').style.color = 'red';
        return;
    }

    try {
        const response = await fetch(`/auth/reset_password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                token: token,
                new_password: newPassword,
                confirm_password: confirmPassword,
            }),
        });

        const data = await response.json();
        const messageDiv = document.getElementById('message');
        if (response.ok) {
            messageDiv.textContent = data.message;
            messageDiv.style.color = 'green';
            setTimeout(() => window.location.href = '/login.html', 2000);
        } else {
            messageDiv.textContent = data.error;
            messageDiv.style.color = 'red';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('message').textContent = 'An error occurred. Please try again later.';
        document.getElementById('message').style.color = 'red';
    }
});

