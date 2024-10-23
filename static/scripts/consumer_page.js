document.addEventListener('DOMContentLoaded', function() {
    // Fetch chef data from the API
    fetch('/api/nearby-chefs')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(chefs => {
            const chefsContainer = document.getElementById('chefsContainer');

            if (chefs.length === 0) {
                chefsContainer.innerHTML = 'No chefs found nearby.';
                return;
            }

            chefs.forEach(chef => {
                // Create a new div for each chef
                const chefCard = document.createElement('div');
                chefCard.classList.add('profile-card');

                // Set the inner HTML for the chef card
                chefCard.innerHTML = `
                    <img src="${chef.image}" alt="${chef.name}" onclick="enlargeProfilePic('${chef.image}')">
                    <h2>${chef.name}</h2>
                    <p>${chef.bio || 'No bio available'}</p>
                    <button class="see-more-btn">See More</button>
                    <button class="explore-food-btn">Explore Food</button>
                    <div class="chef-details hidden">
                        <p><strong>Distance:</strong> ${chef.distance_km} km</p>
                        <p><strong>Cuisine:</strong> ${chef.specialties?.join(', ') || 'Not provided'}</p>
                        <p><strong>WhatsApp:</strong> 
			            <a href="https://wa.me/${chef.whatsapp}" target="_blank" style="color: #25D366; text-decoration: none;">
				                    <i class="fab fa-whatsapp"></i> ${chef.whatsapp || 'Not provided'}
						                </a>
								        </p>
                    </div>
                `;

                // Add event listener for "See More" button
                const seeMoreBtn = chefCard.querySelector('.see-more-btn');
                const chefDetails = chefCard.querySelector('.chef-details');

                seeMoreBtn.addEventListener('click', () => {
                    chefDetails.classList.toggle('hidden');  // Toggle visibility

                    // Check if the details are visible or hidden
                    if (chefDetails.classList.contains('hidden')) {
                        seeMoreBtn.textContent = 'See More'; // Change text to 'See More'
                    } else {
                        seeMoreBtn.textContent = 'Show Less'; // Change text to 'Show Less'
                    }
                });

                // Add event listener for "Explore Food" button
                const exploreFoodBtn = chefCard.querySelector('.explore-food-btn');
                exploreFoodBtn.addEventListener('click', () => {
                    window.location.href = `/api/dishes?chef_id=${chef.chef_id}`;  // Pass chef_id to view_dishes.html
                });

                // Append the chef card to the container
                chefsContainer.appendChild(chefCard);
            });
        })
        .catch(error => {
            console.error('Error fetching chefs:', error);
            const chefsContainer = document.getElementById('chefsContainer');
            chefsContainer.innerHTML = 'Failed to load chefs. Please try again later.';
        });
});

// Function to enlarge profile picture on click
function enlargeProfilePic(imageSrc) {
    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    overlay.innerHTML = `<img src="${imageSrc}" alt="Profile Picture" class="enlarged-image">`;
    document.body.appendChild(overlay);

    overlay.addEventListener('click', () => {
        document.body.removeChild(overlay); // Remove overlay when clicked
    });
}

