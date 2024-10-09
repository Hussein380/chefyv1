export function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    });
                },
                (error) => {
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            alert("You have denied location access. You can continue, but location-based features won't work.");
                            reject(new Error("Permission denied"));
                            break;
                        case error.POSITION_UNAVAILABLE:
                            alert("Location information is unavailable.");
                            reject(new Error("Position unavailable"));
                            break;
                        case error.TIMEOUT:
                            alert("The request to get your location timed out.");
                            reject(new Error("Timeout"));
                            break;
                        case error.UNKNOWN_ERROR:
                            alert("An unknown error occurred.");
                            reject(new Error("Unknown error"));
                            break;
                    }
                },
                {
                    timeout: 10000 // Set a timeout for the location request (e.g., 10 seconds)
                }
            );
        } else {
            alert("Geolocation is not supported by this browser.");
            reject(new Error("Geolocation not supported"));
        }
    });
}

