document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const resultsContent = document.getElementById('resultsContent');
    const emptyState = document.getElementById('emptyState');

    // Function to add a message to the chat
    function addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show loading state
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        loadingDiv.id = 'loadingIndicator';

        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';

        const loadingText = document.createElement('span');
        loadingText.textContent = 'Processing your request...';

        loadingDiv.appendChild(spinner);
        loadingDiv.appendChild(loadingText);

        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to hide loading state
    function hideLoading() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }

    // Function to display results
    function displayResults(results) {
        resultsContent.innerHTML = '';
        emptyState.style.display = 'none';
        resultsContent.style.display = 'block';

        // Sort dates chronologically
        const sortedDates = Object.keys(results).sort((a, b) => new Date(a) - new Date(b));

        sortedDates.forEach(date => {
            const dateCard = document.createElement('div');
            dateCard.className = 'date-card';

            const dateTitle = document.createElement('div');
            dateTitle.className = 'date-title';
            dateTitle.textContent = date;
            dateCard.appendChild(dateTitle);

            const timeSlots = document.createElement('div');
            timeSlots.className = 'time-slots';

            results[date].forEach(time => {
                const timeSlot = document.createElement('span');
                timeSlot.className = 'time-slot';
                timeSlot.textContent = time;
                timeSlots.appendChild(timeSlot);
            });

            dateCard.appendChild(timeSlots);
            resultsContent.appendChild(dateCard);
        });
    }

    // Function to handle sending a message
    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';

            showLoading();

            // Send the message to the server
            fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                addMessage('I\'ve processed your request. Check the results panel to see the available times.', false);
                displayResults(data.result);
            })
            .catch(error => {
                hideLoading();
                addMessage('Sorry, there was an error processing your request. Please try again.', false);
                console.error('Error:', error);
            });
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});