document.addEventListener('DOMContentLoaded', function() {
    console.log('DEBUG_MODE:', window.DEBUG_MODE);  // Add this line to check the value
    const fileUpload = document.getElementById('file-upload');
    const queryInput = document.getElementById('query-input');
    const sendButton = document.getElementById('send-button');
    const messagesContainer = document.getElementById('messages');

    fileUpload.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            addMessage('System', result.message);
        } catch (error) {
            console.error('Upload error:', error);
            addMessage('System', `Error: ${error.message}`);
        }
    });

    async function sendQuery() {
        const query = queryInput.value.trim();
        if (!query) return;

        addMessage('User', query);
        queryInput.value = '';

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Server error: ${errorData.error || response.statusText}`);
            }
            
            const result = await response.json();
            console.log('Search results:', result); // Debug log
            
            if (result.results && result.results.length > 0) {
                addMessage('Assistant', result.results);
            } else {
                addMessage('Assistant', 'No relevant information found.');
            }
        } catch (error) {
            console.error('Query error:', error);
            addMessage('System', `Error: ${error.message}`);
        }
    }

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender.toLowerCase()}`;
        
        // Handle array of results or single text
        if (Array.isArray(text)) {
            messageDiv.textContent = text.join('\n');
        } else {
            messageDiv.textContent = text;
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    sendButton.addEventListener('click', sendQuery);
    queryInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendQuery();
    });
});



async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        addMessage('System', result.message);
    } catch (error) {
        console.error('Upload error:', error);
        addMessage('System', `Error: ${error.message}`);
    }
}

async function sendQuery() {
    const query = queryInput.value.trim();
    if (!query) return;

    addMessage('User', query);
    queryInput.value = '';

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Server error: ${errorData.error || response.statusText}`);
        }
        
        const result = await response.json();
        console.log('Search results:', result); // Debug log
        
        if (result.results && result.results.length > 0) {
            addMessage('Assistant', result.results);
        } else {
            addMessage('Assistant', 'No relevant information found.');
        }
    } catch (error) {
        console.error('Query error:', error);
        addMessage('System', `Error: ${error.message}`);
    }
} 