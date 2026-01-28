// script.js
// --- CONFIGURATION ---
const API_URL = 'http://127.0.0.1:5500/ocr_process'; 

// --- HTML ELEMENT IDS (Ensure these match index.html) ---
const FORM_ID = 'ocr-form';
const FILE_INPUT_ID = 'file-input';
const STATUS_DISPLAY_ID = 'status-message';
const TEXT_DISPLAY_ID = 'extracted-text-display'; 
const MEANING_DISPLAY_ID = 'meaning-display';
const PRONUNCIATION_STATUS_ID = 'pronunciation-status';

// --- EVENT LISTENER ---
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById(FORM_ID);
    if (form) {
        form.addEventListener('submit', handleUpload);
    } else {
        console.error(`Error: Form element with ID "${FORM_ID}" not found.`);
    }
});


async function handleUpload(event) {
    event.preventDefault(); 

    const fileInput = document.getElementById(FILE_INPUT_ID);
    const file = fileInput.files[0];

    clearResults();
    setStatus("Processing image...", true);

    if (!file) {
        alert("Please select an image file first.");
        setStatus("Ready to upload.");
        return;
    }

    try {
        const formData = new FormData();
        formData.append('image', file); 
        
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: response.statusText }));
            const errorMessage = errorData.detail || "An unknown error occurred on the server.";
            alert("Error processing image: " + errorMessage);
            setStatus(`Error: ${errorMessage}`, false);
            return;
        }

        const data = await response.json(); 

        if (data.status === 'success') {
            setStatus("Extraction Successful!");
            displayResults(data);
        } else {
            const errorMessage = data.detail || "Server returned failure status.";
            alert("Error processing image: " + errorMessage);
            setStatus(`Error: ${errorMessage}`, false);
        }

    } catch (error) {
        console.error('Fetch Error:', error);
        alert("Could not connect to the API server. Please ensure the backend is running at " + API_URL);
        setStatus("Connection Failed. Check console for details.", false);
    }
}


function displayResults(data) {
    document.getElementById(TEXT_DISPLAY_ID).textContent = data.extracted_text || 'No text extracted.';
    document.getElementById(MEANING_DISPLAY_ID).textContent = data.translated_meaning || 'Meaning unavailable.';

    const audioStatusElement = document.getElementById(PRONUNCIATION_STATUS_ID);
    
    if (data.pronunciation_audio) {
        // Create a data URL for the MP3 audio
        const audioDataUrl = `data:audio/mp3;base64,${data.pronunciation_audio}`;
        
        // Create and insert an <audio> element
        audioStatusElement.innerHTML = `
            <audio controls autoplay>
                <source src="${audioDataUrl}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        `;
    } else {
        audioStatusElement.textContent = 'Audio generation unavailable.';
    }
}

function clearResults() {
    document.getElementById(TEXT_DISPLAY_ID).textContent = '';
    document.getElementById(MEANING_DISPLAY_ID).textContent = '';
    document.getElementById(PRONUNCIATION_STATUS_ID).innerHTML = ''; // Use innerHTML to clear audio element
}

function setStatus(message, isLoading = false) {
    const statusElement = document.getElementById(STATUS_DISPLAY_ID);
    if (statusElement) {
        statusElement.textContent = message;
    }
}





