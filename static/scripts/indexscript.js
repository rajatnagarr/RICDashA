// Function to handle button click and redirection
function redirectToPage(buttonId, pageUrl) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.addEventListener("click", function () {
            window.location.href = pageUrl; // Redirect to the specified page
        });
    }
}

// Call redirectToPage for each button and its corresponding page URL
redirectToPage('pods-button', 'ric.html');
redirectToPage('sdl-button', 'redis.html');
