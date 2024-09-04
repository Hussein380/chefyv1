document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profileForm');

    profileForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(profileForm);
        const data = {
            username: formData.get('username'),
            bio: formData.get('bio'),
            whatsapp: formData.get('whatsapp'),
            location_enabled: formData.get('location_enabled') === 'on',
        };

        try {
            const response = await fetch('/api/chef/update-profile', {
                method: 'POST',
                body: formData,  // Use FormData to include both text and file data
            });

            if (!response.ok) {
                throw new Error('Error updating profile');
            }

            const result = await response.json();
            if (result.success) {
                alert('Profile updated successfully');
            } else {
                alert(result.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error updating profile:', error);
        }
    });
});

