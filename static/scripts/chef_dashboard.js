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

