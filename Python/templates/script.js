//Code for list out the Languages

const languages = [
    { name: "English", code: "en" },
    { name: "Spanish", code: "es" },
    { name: "French", code: "fr" },
    // Add more languages as needed
];

// Function to populate the dropdown
function populateDropdown() {
    const dropdown = document.getElementById("languageDropdown");

    languages.forEach((lang) => {
        const option = document.createElement("option");
        option.value = lang.code;
        option.textContent = lang.name;
        dropdown.appendChild(option);
    });
}

// Call the function to populate the dropdown
populateDropdown();