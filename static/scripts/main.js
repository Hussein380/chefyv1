document.getElementById('chefs-link').addEventListener('click', function(event) {
    console.log("Chef link clicked"); // Log to see if the event is firing
    event.preventDefault(); // Prevent default anchor click behavior

    fetch('/auth/check_login_status') // Check login status
        .then(response => response.json())
        .then(data => {
            console.log("Login status response:", data); // Log the response data
            if (data.is_logged_in) {
                // Redirect based on user role
                if (data.role === 'chef') {
                    window.location.href = '/chef_dashboard.html'; // Correct route for chef dashboard
                } else if (data.role === 'consumer') {
                    window.location.href = '/consumer'; // Adjust to your actual route for displaying chef profiles
                }
            } else {
                // Redirect to signup page
                window.location.href = '/signup'; // Adjust to your actual URL
            }
        })
        .catch(error => console.error('Error checking login status:', error));
});
