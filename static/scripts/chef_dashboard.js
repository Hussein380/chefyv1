document.addEventListener('DOMContentLoaded', () => {
    // Select elements
    const profileForm = document.getElementById('profileForm');
    const deleteProfileButton = document.getElementById('deleteProfile');
    const locationToggle = document.getElementById('locationToggle');
    const uploadPicture = document.getElementById('uploadPicture');
    const loadingIndicator = document.getElementById('loadingIndicator'); // Select loading indicator

    // Function to preview the profile picture
    function previewProfileImage(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                document.getElementById('profileImagePreview').src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    }

    // Function to handle profile retrieval
    function getProfile() {
        fetch('/api/chef/profile')
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                document.getElementById('username').value = data.username;
                document.getElementById('bio').value = data.bio;
                document.getElementById('whatsapp').value = data.whatsapp;
                document.getElementById('profileImagePreview').src = data.profile_picture ? `/uploads/${data.profile_picture}` : '/static/images/default_profile.jpg';
                locationToggle.checked = data.location_enabled;
            } else {
                // Redirect to the dashboard to create a profile
                alert('Profile not found. Please create a profile');
            }
        });
    }

    // Function to create profile
    function createProfile(profileData, profilePicture) {
        const formData = new FormData();
        formData.append('username', profileData.username);
        formData.append('bio', profileData.bio);
        formData.append('whatsapp', profileData.whatsapp);
        formData.append('location_enabled', profileData.location_enabled);
        if (profilePicture) {
            formData.append('profile_picture', profilePicture);
        }

        // Show loading spinner
        loadingIndicator.style.display = 'block';

        fetch('/api/chef/create_profile', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = 'none'; // Hide loading spinner
            if (data.success) {
                alert('Profile created successfully!');
                // Optionally redirect to profile page or dashboard
            } else {
                alert(data.error);
            }
        });
    }

    // Function to show toast messages
    function showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`; // 'toast' is a base class, type can be 'success' or 'error'
        toast.innerText = message;
        document.body.appendChild(toast);
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 3000); // Remove after 3 seconds
    }

    // Function to handle profile updates
    function updateProfile(profileData, profilePicture) {
        const formData = new FormData();
        formData.append('username', profileData.username);
        formData.append('bio', profileData.bio);
        formData.append('whatsapp', profileData.whatsapp);
        formData.append('location_enabled', profileData.location_enabled);
        if (profilePicture) {
            formData.append('profile_picture', profilePicture);
        }

        // Show loading spinner
        loadingIndicator.style.display = 'block';

        fetch('/api/chef/update-profile', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = 'none'; // Hide loading spinner
            if (data.success) {
                alert('Profile updated successfully!');
            } else {
                alert(data.error);
            }
        });
    }

    // Function to handle profile deletion
    function deleteProfile() {
        fetch('/api/chef/delete-profile', {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Profile deleted successfully!');
                // Optionally redirect or clear form
            } else {
                alert(data.error);
            }
        });
    }

    // Event listeners
    profileForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const profileData = {
            username: document.getElementById('username').value,
            bio: document.getElementById('bio').value,
            whatsapp: document.getElementById('whatsapp').value,
            location_enabled: locationToggle.checked
        };
        const profilePicture = uploadPicture.files[0];

        // Decide whether to create or update profile
        fetch('/api/chef/profile')
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                updateProfile(profileData, profilePicture);
            } else {
                createProfile(profileData, profilePicture);
            }
        });
    });

    deleteProfileButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to delete your profile?')) {
            deleteProfile();
        }
    });

    // Add event listener for profile picture upload
    uploadPicture.addEventListener('change', previewProfileImage);

    // Load profile data when the page is loaded
    getProfile();
});

