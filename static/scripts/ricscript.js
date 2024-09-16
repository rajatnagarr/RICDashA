// This function runs once the DOM is fully loaded.
document.addEventListener("DOMContentLoaded", function() {

    // Setting an interval to update data every second.
    setInterval(() => {
        // Fetching and displaying data for specific sections.
        fetchJSON('/getOnboarded', 'onboarded-xapps-content');
        fetchJSON('/getDeployed', 'deployed-xapps-content');
        fetchJSON('/getE2Nodes', 'gnb-data-content');
        fetchJSON('/getUE', 'ue-prb-data-content');
        fetchText('/getpltPods', 'plat-content');
        fetchText('/getxappPods', 'xapps-content');
    }, 1000); // Interval set to 1 second.
});

// Function to fetch and display data for functions that return valid JSONs.
function fetchJSON(apiEndpoint, elementId) {
    // Fetching data from the given API endpoint.
    fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
            const element = document.getElementById(elementId);
            // If the element is found, update its content.
            if (element) {
                element.textContent = JSON.stringify(data, null, 2);
            } else {
                console.log("Element not found:", elementId);
            }
        })
        .catch(error => console.error(`JSON: Error fetching data for #${elementId}:`, error));
}

// Function to fetch and display data for functions that can only return strings.
function fetchText(apiEndpoint, elementId) {
    // Fetching data from the given API endpoint.
    fetch(apiEndpoint)
        .then(response => response.text())
        .then(data => {
            const element = document.getElementById(elementId);
            // If the element is found, update its content.
            if (element) {
                element.textContent = data;
            } else {
                console.log("Element not found:", elementId);
            }
        })
        .catch(error => console.error(`Text: Error fetching data for #${elementId}:`, error));
}