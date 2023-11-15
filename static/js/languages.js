function change_page_texts(data) {

    // Iterate over the keys in jsonData
    $.each(data, function(key, value) {
        // Update the content of the HTML element with the corresponding ID
        $("#" + key).text(value);
    });
}

function fastTranslation(textData, sourceLanguage, selectedLanguage) {
    fetch('http://127.0.0.1:5000/fast_translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify({ "text": textData, "sourceLanguage":sourceLanguage, "selectedLanguage": selectedLanguage }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        change_page_texts(data)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getTextFromIds() {
    var idList = ["book-title", "book-author", "delete-book-link", "edit-book", "book-description-title", "book-description"];
    var textData = {};

    // Gather text content from elements with specific IDs
    idList.forEach(function (elementId) {
        var $element = $("#" + elementId);
        var text = $element.text().trim();

        if (text.length > 0) {
            textData[elementId] = text;
        }
    });

    return textData;
}

function translateText(textData, sourceLanguage, selectedLanguage) {
    fetch('http://127.0.0.1:5000/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify({ "text": textData, "sourceLanguage": sourceLanguage, "selectedLanguage": selectedLanguage }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        change_page_texts(data)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to get the value of a cookie by name
function getCookie(cookieName) {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === cookieName) {
            return decodeURIComponent(value);
        }
    }
    return null;
}

// Function to handle saving the selected language
function saveLanguage() {
    // source language
    let sourceLanguage = getCookie('source_language');
    let selectedLanguage = getCookie('selectedLanguage');

    if (selectedLanguage === null) {
        // if here, it means that no translations has been achieved
        // because selectedLanguage is null. So, we set the selecteddLanguage

        // value extraction of selected language
        selectedLanguage = languageSelect.value;
        // saving the language as client session cookie
        document.cookie = `selectedLanguage=${selectedLanguage}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;
        console.log('Selected language:', selectedLanguage);

    } else {

        // if here, it means that at least one translation has been achieved
        // because selectedLanguage is not null. So, we change the source language
        // and then we set the new selecteddLanguage cookie
        sourceLanguage = selectedLanguage;
        document.cookie = `source_language=${sourceLanguage}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;
        
        // value extraction of selected language
        selectedLanguage = languageSelect.value;
        // saving the language as client session cookie
        document.cookie = `selectedLanguage=${selectedLanguage}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;

    }
    
    // modal closure
    $('#languageModal').modal('hide');

    // Use the value as needed
    var textData = getTextFromIds();
    //fastTranslation(textData, sourceLanguage, selectedLanguage);
    translateText(textData, sourceLanguage, selectedLanguage);
}


const languages = ['Afrikaans', 'Arabic', 'Armenian', 'Azerbaijani', 'Belarusian', 'Bosnian', 'Bulgarian', 'Catalan', 'Chinese', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'Finnish', 'French', 'Galician', 'German', 'Greek', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 'Italian', 'Japanese', 'Kannada', 'Kazakh', 'Korean', 'Latvian', 'Lithuanian', 'Macedonian', 'Malay', 'Marathi', 'Maori', 'Nepali', 'Norwegian', 'Persian', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Serbian', 'Slovak', 'Slovenian', 'Spanish', 'Swahili', 'Swedish', 'Tagalog', 'Tamil', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Vietnamese', 'Welsh'];

const languageSelect = document.getElementById('languageSelect');

// Populate the select element with the specified list of languages
languages.forEach(language => {
    const option = document.createElement('option');
    option.value = language.toLowerCase();
    option.textContent = language;
    languageSelect.appendChild(option);
});