document.addEventListener('DOMContentLoaded', function() {
    async function fetchProfile() {
        try {
            const response = await fetch('/api/chef/profile');
            if (!response.ok) {
                throw new Error('Profile not found');
            }
            const profile = await response.json();
            populateProfileForm(profile);
        } catch (error) {
            console.error('Error fetching profile:', error);
        }
    }

    function populateProfileForm(profile) {
        document.querySelector('input[name="username"]').value = profile.username;
        document.querySelector('textarea[name="bio"]').value = profile.bio;
        document.querySelector('input[name="whatsapp"]').value = profile.whatsapp;
        document.querySelector('input[name="location_enabled"]').checked = profile.location_enabled;
        const profilePictureImg = document.querySelector('#profilePicture');
        profilePictureImg.src = profile.profile_picture || '/static/assets/default_profile.jpg';
    }

    fetchProfile();
});

