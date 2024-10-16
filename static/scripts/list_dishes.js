function deleteDish(dishId) {
    if (confirm("Are you sure you want to delete this dish?")) {
        fetch(`/delete_dish/${dishId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the dish from the list
                const dishElement = document.getElementById(`dish-${dishId}`);
                dishElement.remove();
            } else {
                alert("Failed to delete dish.");
            }
        })
        .catch(error => console.error('Error deleting dish:', error));
    }
}

