// static/scripts/signup.js

import { getUserLocation } from './geolocation.js'; // Import the getUserLocation function

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

        // Try to get user's location
        getUserLocation()
            .then(location => {
                // Proceed with signup and send location data
                sendSignupRequest(email, password, confirmPassword, role, location.latitude, location.longitude);
            })
            .catch(error => {
                console.error('Error getting location:', error);
                // Continue with signup without location
                sendSignupRequest(email, password, confirmPassword, role, null, null);
            });
    });

    // Function to send signup request to the server
    function sendSignupRequest(email, password, confirmPassword, role, latitude, longitude) {
        // Send sign-up request with or without location data
        fetch('/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password,
                confirm_password: confirmPassword,
                role,
                latitude,
                longitude
            })
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
    }
});
