document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signup-form');

    signupForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        // Get form data
        const formData = new FormData(signupForm);
        const email = formData.get('email');
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm-password');
        const role = formData.get('role');

        // Validate password match
        if (password !== confirmPassword) {
            alert("Passwords do not match. Please try again.");
            return;
        }

        // Send sign-up request
        fetch('/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password, confirm_password: confirmPassword, role })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                window.location.href = data.redirect_url; // Redirect to appropriate page based on role
            } else {
                alert(data.error); // Display error message
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

