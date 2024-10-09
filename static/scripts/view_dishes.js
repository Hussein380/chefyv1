function likeDish(dishId) {
    // Get the current likes count from the HTML element
    let likesCountElement = document.getElementById(`likes-count-${dishId}`);
    let currentLikes = parseInt(likesCountElement.innerText);

    // Send the POST request to the server to register the like
    fetch(`/api/dish/like/${dishId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // If the server successfully registers the like, increment the count
        if (data.success) {
            likesCountElement.innerText = currentLikes + 1;
        } else {
            console.error('Error liking the dish:', data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

