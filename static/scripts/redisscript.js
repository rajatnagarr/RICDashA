// This function runs once the DOM is fully loaded.
document.addEventListener("DOMContentLoaded", function() {
    const routeRedis = '/accessRedis';
    const contentArea = document.querySelector('.full-page-background'); // Define contentArea

    function fetchAndUpdateData() {
        fetch(routeRedis)
            .then(response => response.json())
            .then(responseData => {
                const organizedData = responseData.data;
                createOrUpdateSections(organizedData, contentArea);
                setTimeout(fetchAndUpdateData, 1000); // Schedule the next update after 1 second
            })
            .catch(error => console.error('Error:', error));
    }

    fetchAndUpdateData(); // Start the initial fetch and update process
});

function createOrUpdateSections(organizedData, contentArea) {
    // Iterating over each key in the organized data.
    Object.keys(organizedData).forEach((key) => {
        let mainSection = document.getElementById(`section-${key}`);

        // Check if the section already exists.
        if (!mainSection) {
            mainSection = document.createElement('details');
            mainSection.id = `section-${key}`;
            mainSection.className = 'section';

            const titleSummary = document.createElement('summary');
            titleSummary.textContent = key;
            titleSummary.className = 'section-title';

            mainSection.appendChild(titleSummary);
            contentArea.appendChild(mainSection);
        }

        // Creating or updating subsections for each key.
        organizedData[key].forEach(subItem => {
            const subsectionId = `subsection-${key}-${subItem[0]}`;
            let subsection = document.getElementById(subsectionId);

            if (!subsection) {
                subsection = document.createElement('details');
                subsection.id = subsectionId;
                subsection.className = 'subsection';

                const subTitleSummary = document.createElement('summary');
                subTitleSummary.textContent = subItem[0];
                subTitleSummary.addEventListener('click', function(event) {
                    event.stopPropagation();
                });
                subsection.appendChild(subTitleSummary);

                const formattedTextDiv = document.createElement('div');
                formattedTextDiv.className = 'formatted-text';
                subsection.appendChild(formattedTextDiv);

                mainSection.appendChild(subsection);
            }

            // Update the text content of the subsection.
            let content = subItem[1];
            let formattedContent = '';

            if (Array.isArray(content)) {
                // If the content is an array, format each item as JSON if possible.
                formattedContent = content.map(item => {
                    if (typeof item === 'object') {
                        return JSON.stringify(item, null, 2);
                    } else {
                        return item;
                    }
                }).join('\n');
            } else if (typeof content === 'object') {
                // If the content is an object, format it as JSON.
                formattedContent = JSON.stringify(content, null, 2);
            } else {
                // If the content is a string, limit its length if necessary.
                formattedContent = content.length > 1000 ? content.substring(0, 1000) : content;
            }

            const formattedTextDiv = subsection.querySelector('.formatted-text');
            formattedTextDiv.innerHTML = ''; // Clear the existing content
            const paragraph = document.createElement('pre');
            paragraph.textContent = formattedContent;
            formattedTextDiv.appendChild(paragraph);
        });
    });
}
}
