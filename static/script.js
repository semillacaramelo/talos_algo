// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const statusDisplay = document.getElementById('status-display');
    const startButton = document.getElementById('start-button');
    const stopButton = document.getElementById('stop-button');
    const instrumentValue = document.getElementById('instrument-value');
    const durationValue = document.getElementById('duration-value');
    const stakeValue = document.getElementById('stake-value');
    const balanceValue = document.getElementById('balance-value');
    const activeTradesValue = document.getElementById('active-trades-value');
    const logOutput = document.getElementById('log-output');
    const clearLogsButton = document.getElementById('clear-logs');

    // Store existing logs to avoid duplicates
    let existingLogs = new Set();

    // Function to fetch from API and handle response
    async function fetchFromAPI(endpoint) {
        try {
            const response = await fetch(endpoint);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Fetch error: ${error.message}`);
            return null;
        }
    }

    // Update status display
    function updateStatusDisplay(status) {
        statusDisplay.textContent = `Status: ${status}`;
        
        // Update alert class based on status
        statusDisplay.className = 'alert';
        if (status === 'Running') {
            statusDisplay.classList.add('alert-success');
        } else if (status === 'Stopping' || status === 'Starting bot...') {
            statusDisplay.classList.add('alert-warning');
        } else if (status === 'Error') {
            statusDisplay.classList.add('alert-danger');
        } else {
            statusDisplay.classList.add('alert-secondary');
        }
    }

    // Update configuration display
    function updateConfigDisplay(config) {
        instrumentValue.textContent = config.instrument;
        durationValue.textContent = config.duration;
        stakeValue.textContent = config.stake;
    }

    // Update live state display
    function updateStateDisplay(balance, activeTrades) {
        balanceValue.textContent = balance;
        activeTradesValue.textContent = activeTrades;
    }

    // Update log output
    function updateLogOutput(logs) {
        if (!logs || !logs.length) return;
        
        let newContent = '';
        logs.forEach(log => {
            if (!existingLogs.has(log)) {
                existingLogs.add(log);
                newContent += log + '\n';
            }
        });
        
        // Append new logs to the existing content
        if (newContent) {
            logOutput.textContent += newContent;
            // Auto-scroll to bottom
            logOutput.scrollTop = logOutput.scrollHeight;
        }
    }

    // Fetch and update status
    async function fetchStatus() {
        const data = await fetchFromAPI('/get_status');
        if (data) {
            updateStatusDisplay(data.status);
            updateConfigDisplay(data.config);
            updateStateDisplay(data.balance, data.active_trades);
        }
    }

    // Connect to log stream
    function connectLogStream() {
        const eventSource = new EventSource('/stream_logs');
        
        eventSource.onmessage = function(event) {
            const logs = JSON.parse(event.data);
            logs.forEach(log => {
                const logEntry = `[${log.timestamp}] ${log.level}: ${log.message}`;
                if (!existingLogs.has(logEntry)) {
                    existingLogs.add(logEntry);
                    logOutput.textContent += logEntry + '\n';
                    logOutput.scrollTop = logOutput.scrollHeight;
                }
            });
        };

        eventSource.onerror = function(error) {
            console.error("Log stream error:", error);
            eventSource.close();
            // Attempt to reconnect after 5 seconds
            setTimeout(connectLogStream, 5000);
        };
    }

    // Event listener for Start button
    startButton.addEventListener('click', async function() {
        const data = await fetchFromAPI('/start_bot');
        if (data) {
            updateStatusDisplay(data.status);
            console.log('Bot start command sent:', data);
            
            // Add to logs
            const logEntry = `[${new Date().toLocaleTimeString()}] ${data.status}`;
            updateLogOutput([logEntry]);
        }
    });

    // Event listener for Stop button
    stopButton.addEventListener('click', async function() {
        const data = await fetchFromAPI('/stop_bot');
        if (data) {
            updateStatusDisplay(data.status);
            console.log('Bot stop command sent:', data);
            
            // Add to logs
            const logEntry = `[${new Date().toLocaleTimeString()}] ${data.status}`;
            updateLogOutput([logEntry]);
        }
    });

    // Event listener for Clear Logs button
    clearLogsButton.addEventListener('click', function() {
        logOutput.textContent = '';
        existingLogs.clear();
    });

    // Initial fetch and stream setup
    fetchStatus();
    connectLogStream();

    // Periodic status updates
    setInterval(fetchStatus, 5000);  // Every 5 seconds
});
