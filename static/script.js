// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const statusDisplay = document.getElementById('status-display');
    const connectionStatus = document.getElementById('connection-status');
    const startButton = document.getElementById('start-button');
    const stopButton = document.getElementById('stop-button');
    const strategySelect = document.getElementById('strategy-select');
    const modelSelect = document.getElementById('model-select');
    const switchAccountButton = document.getElementById('switch-account-type');
    const resetStatsButton = document.getElementById('reset-stats');
    const switchThemeButton = document.getElementById('switch-theme');
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    const htmlRoot = document.getElementById('html-root');
    const bootstrapTheme = document.getElementById('bootstrap-theme');
    const darkThemeCss = document.getElementById('theme-css');
    const lightThemeCss = document.getElementById('light-theme-css');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    // Apply saved theme on page load
    if (savedTheme === 'light') {
        applyLightTheme();
    }
    
    // Configuration elements
    const instrumentValue = document.getElementById('instrument-value');
    const durationValue = document.getElementById('duration-value');
    const stakeValue = document.getElementById('stake-value');
    const maxTradesValue = document.getElementById('max-trades-value');
    
    // Stats elements
    const balanceValue = document.getElementById('balance-value');
    const dailyPnlValue = document.getElementById('daily-pnl-value');
    const activeTradesValue = document.getElementById('active-trades-value');
    const winRateValue = document.getElementById('win-rate-value');
    
    // Model status elements
    const lastSignalValue = document.getElementById('last-signal-value');
    const lastPriceValue = document.getElementById('last-price-value');
    const uptimeValue = document.getElementById('uptime-value');
    const featureCountValue = document.getElementById('feature-count-value');
    const lastTradeValue = document.getElementById('last-trade-value');
    
    // Trade table
    const activeTradesTable = document.getElementById('active-trades-table');
    
    // Logs
    const logOutput = document.getElementById('log-output');
    const clearLogsButton = document.getElementById('clear-logs');

    // Store existing logs to avoid duplicates
    let existingLogs = new Set();
    let currentTrades = [];
    let winCount = 0;
    let lossCount = 0;

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
            updateConnectionStatus(false);
            return null;
        }
    }

    // Update connection status
    function updateConnectionStatus(isConnected) {
        connectionStatus.className = isConnected ? 
            'connection-dot connected' : 
            'connection-dot disconnected';
        connectionStatus.title = isConnected ? 
            'API Connected' : 
            'API Disconnected';
    }

    // Update status display
    function updateStatusDisplay(status) {
        // Update connection status first
        updateConnectionStatus(true);
        
        // Clear previous content and add icon
        statusDisplay.innerHTML = '';
        const icon = document.createElement('i');
        icon.className = 'fas me-2';
        
        if (status === 'Running') {
            icon.classList.add('fa-play-circle');
            // Disable start button, enable stop button
            if (startButton) startButton.disabled = true;
            if (stopButton) stopButton.disabled = false;
        } else if (status === 'Stopping' || status === 'Starting bot...') {
            icon.classList.add('fa-sync-alt');
            icon.style.animation = 'fa-spin 2s infinite linear';
        } else if (status === 'Error') {
            icon.classList.add('fa-exclamation-circle');
        } else {
            icon.classList.add('fa-info-circle');
            // Enable start button, disable stop button
            if (startButton) startButton.disabled = false;
            if (stopButton) stopButton.disabled = true;
        }
        
        statusDisplay.appendChild(icon);
        statusDisplay.append(`Status: ${status}`);
        
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
        // If we have configurable inputs, update their values
        if (window.instrumentInput) {
            instrumentInput.value = config.instrument || '';
        } else if (instrumentValue) {
            instrumentValue.textContent = config.instrument || 'N/A';
        }
        
        if (window.durationInput) {
            durationInput.value = config.duration || '';
        } else if (durationValue) {
            durationValue.textContent = `${config.duration || '0'} ${config.duration_unit || 't'}`;
        }
        
        if (window.durationUnitSelect) {
            durationUnitSelect.value = config.duration_unit || 't';
        }
        
        if (window.stakeInput) {
            stakeInput.value = config.stake || '';
        } else if (stakeValue) {
            stakeValue.textContent = `${config.stake || '0'} ${config.currency || 'USD'}`;
        }
        
        // Optional value update if the field exists
        if (maxTradesValue) {
            maxTradesValue.textContent = config.max_concurrent_trades || '3';
        }
    }

    // Update live state display with all the enhanced data
    function updateStateDisplay(data) {
        // Basic data
        if (balanceValue) balanceValue.textContent = data.balance || 'N/A';
        if (activeTradesValue) activeTradesValue.textContent = data.active_trades || '0';
        if (lastPriceValue) lastPriceValue.textContent = data.last_price || 'N/A';
        
        // Model status
        if (window.modelStatusValue) {
            modelStatusValue.textContent = data.model_status || 'N/A';
            // Add color indicating status
            modelStatusValue.className = 'badge';
            if (data.model_status === 'Loaded') {
                modelStatusValue.classList.add('bg-success');
            } else if (data.model_status && data.model_status.includes('Error')) {
                modelStatusValue.classList.add('bg-danger');
            } else if (data.model_status === 'Loading...') {
                modelStatusValue.classList.add('bg-warning');
            } else {
                modelStatusValue.classList.add('bg-secondary');
            }
        }
        
        // Model file
        if (window.modelFileValue) {
            modelFileValue.textContent = data.model_file || 'N/A';
        }
        
        // Update last signal with appropriate styling
        if (lastSignalValue) {
            lastSignalValue.textContent = data.last_signal || 'N/A';
            lastSignalValue.className = 'badge';
            
            if (data.last_signal === 'BUY') {
                lastSignalValue.classList.add('bg-success');
            } else if (data.last_signal === 'SELL') {
                lastSignalValue.classList.add('bg-danger');
            } else {
                lastSignalValue.classList.add('bg-secondary');
            }
        }
        
        // Other status values
        if (uptimeValue) uptimeValue.textContent = data.uptime || 'N/A';
        if (featureCountValue) featureCountValue.textContent = data.feature_count || 'N/A';
        if (lastTradeValue) lastTradeValue.textContent = data.last_trade || 'N/A';
        
        // Update win/loss counts and win rate
        if (window.winCount) winCount = data.win_count || 0;
        if (window.lossCount) lossCount = data.loss_count || 0;
        
        // Calculate win rate
        if (winRateValue) {
            const totalTrades = (data.win_count || 0) + (data.loss_count || 0);
            if (totalTrades > 0) {
                const rate = Math.floor((data.win_count / totalTrades) * 100);
                winRateValue.textContent = `${rate}%`;
            } else {
                winRateValue.textContent = '0%';
            }
        }
        
        // Update daily P&L if available
        if (data.daily_pnl !== undefined && dailyPnlValue) {
            const pnl = data.daily_pnl;
            dailyPnlValue.textContent = pnl >= 0 ? 
                `+$${pnl.toFixed(2)}` : 
                `-$${Math.abs(pnl).toFixed(2)}`;
            dailyPnlValue.className = 'stat-value';
            dailyPnlValue.classList.add(pnl >= 0 ? 'text-success' : 'text-danger');
        }
    }

    // Update active trades table
    function updateTradesTable(trades) {
        if (!activeTradesTable) return;
        
        // Clear the table
        activeTradesTable.innerHTML = '';
        
        if (!trades || trades.length === 0) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.colSpan = 6;
            cell.className = 'text-center';
            cell.textContent = 'No active trades';
            row.appendChild(cell);
            activeTradesTable.appendChild(row);
        } else {
            trades.forEach(trade => {
                const row = document.createElement('tr');
                
                // ID
                const idCell = document.createElement('td');
                idCell.textContent = trade.id.substring(0, 8) + '...';
                
                // Type (CALL/PUT)
                const typeCell = document.createElement('td');
                typeCell.textContent = trade.type;
                typeCell.className = trade.type === 'CALL' ? 'text-success' : 'text-danger';
                
                // Entry price
                const entryCell = document.createElement('td');
                entryCell.textContent = trade.entry_price.toFixed(4);
                
                // Current price
                const currentCell = document.createElement('td');
                currentCell.textContent = trade.current_price.toFixed(4);
                
                // P&L
                const pnlCell = document.createElement('td');
                const pnl = trade.pnl || 0;
                pnlCell.textContent = pnl > 0 ? `+$${pnl.toFixed(2)}` : `-$${Math.abs(pnl).toFixed(2)}`;
                pnlCell.className = pnl >= 0 ? 'text-success' : 'text-danger';
                
                // Time remaining
                const timeCell = document.createElement('td');
                timeCell.textContent = trade.time_remaining || 'N/A';
                
                // Add cells to row
                row.appendChild(idCell);
                row.appendChild(typeCell);
                row.appendChild(entryCell);
                row.appendChild(currentCell);
                row.appendChild(pnlCell);
                row.appendChild(timeCell);
                
                // Add row to table
                activeTradesTable.appendChild(row);
            });
        }
    }

    // Update log output
    function updateLogOutput(logs) {
        if (!logs || !logs.length) return;
        
        logs.forEach(log => {
            const logEntry = `[${log.timestamp}] ${log.level}: ${log.message}`;
            if (!existingLogs.has(logEntry)) {
                existingLogs.add(logEntry);
                logOutput.textContent += logEntry + '\n';
                logOutput.scrollTop = logOutput.scrollHeight;
                
                // Update win/loss count based on log messages
                if (log.message.includes('Trade successful') || log.message.includes('Contract won')) {
                    winCount++;
                } else if (log.message.includes('Trade failed') || log.message.includes('Contract lost')) {
                    lossCount++;
                }
            }
        });
    }

    // Fetch logs using polling instead of SSE
    async function fetchLogs() {
        const logs = await fetchFromAPI('/logs');
        if (logs) {
            updateLogOutput(logs);
        }
        // Poll again after 1 second
        setTimeout(fetchLogs, 1000);
    }

    // Fetch and update status
    async function fetchStatus() {
        const data = await fetchFromAPI('/get_status');
        if (data) {
            updateStatusDisplay(data.status);
            updateConfigDisplay(data.config);
            updateStateDisplay(data);
            
            // Update trades table if we have trade data
            if (data.trades) {
                currentTrades = data.trades;
                updateTradesTable(data.trades);
            }
        }
    }

    // Implement Server-Sent Events (SSE) for log streaming
    function setupLogStreaming() {
        // Check if EventSource is supported
        if (typeof EventSource === "undefined") {
            console.warn("EventSource is not supported, falling back to polling");
            fetchLogs();
            return;
        }
        
        const eventSource = new EventSource('/stream_logs');
        
        eventSource.onmessage = function(event) {
            try {
                const logData = JSON.parse(event.data);
                updateLogOutput([logData]);
            } catch (error) {
                console.error("Error parsing log event:", error);
            }
        };
        
        eventSource.onerror = function(error) {
            console.error("EventSource error:", error);
            eventSource.close();
            // Fall back to polling if SSE fails
            setTimeout(() => {
                console.log("Attempting to reconnect SSE...");
                setupLogStreaming();
            }, 5000);
        };
    }

    // Initialize price chart
    let priceChart = null;

    function setupPriceChart() {
        const ctx = document.getElementById('priceChart');
        if (!ctx) return;
        
        // Check if Chart.js is loaded
        if (typeof Chart === 'undefined') {
            console.error("Chart.js is not loaded");
            return;
        }
        
        priceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [], // x-axis labels (timestamps)
                datasets: [{
                    label: 'Price',
                    data: [], // y-axis data (prices)
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    pointRadius: 1,
                    pointHoverRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: {
                            maxTicksLimit: 10,
                            maxRotation: 0
                        }
                    },
                    y: {
                        beginAtZero: false
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        enabled: true
                    }
                },
                animation: {
                    duration: 0 // Disable animation for better performance
                }
            }
        });
        
        // Start updating chart data
        fetchChartData();
    }

    // Fetch chart data from the server
    async function fetchChartData() {
        if (!priceChart) return;
        
        try {
            const response = await fetch('/get_chart_data');
            if (!response.ok) {
                throw new Error('Failed to fetch chart data');
            }
            
            const chartData = await response.json();
            
            if (chartData && chartData.length > 0) {
                // Format the data for Chart.js
                const times = chartData.map(point => {
                    // Format timestamp to readable time (HH:MM:SS)
                    const date = new Date(point.time * 1000);
                    return date.toLocaleTimeString();
                });
                
                const prices = chartData.map(point => point.price);
                
                // Limit data points for better performance
                const maxPoints = 100;
                if (times.length > maxPoints) {
                    times.splice(0, times.length - maxPoints);
                    prices.splice(0, times.length - maxPoints);
                }
                
                // Update the chart data
                priceChart.data.labels = times;
                priceChart.data.datasets[0].data = prices;
                priceChart.update();
            }
        } catch (error) {
            console.error('Error fetching chart data:', error);
        }
        
        // Schedule the next update
        setTimeout(fetchChartData, 2000);
    }

    // Event listener for Start button
    startButton.addEventListener('click', async function() {
        const data = await fetchFromAPI('/start_bot');
        if (data) {
            updateStatusDisplay(data.status);
            console.log('Bot start command sent:', data);
            
            // Add to logs
            const logEntry = `[${new Date().toLocaleTimeString()}] INFO: Bot starting with strategy: ${strategySelect.value}, model: ${modelSelect.value}`;
            if (!existingLogs.has(logEntry)) {
                existingLogs.add(logEntry);
                logOutput.textContent += logEntry + '\n';
                logOutput.scrollTop = logOutput.scrollHeight;
            }
        }
    });

    // Event listener for Stop button
    stopButton.addEventListener('click', async function() {
        const data = await fetchFromAPI('/stop_bot');
        if (data) {
            updateStatusDisplay(data.status);
            console.log('Bot stop command sent:', data);
            
            // Add to logs
            const logEntry = `[${new Date().toLocaleTimeString()}] INFO: Bot stopping`;
            if (!existingLogs.has(logEntry)) {
                existingLogs.add(logEntry);
                logOutput.textContent += logEntry + '\n';
                logOutput.scrollTop = logOutput.scrollHeight;
            }
        }
    });

    // Event listener for Clear Logs button
    clearLogsButton.addEventListener('click', function() {
        logOutput.textContent = '';
        existingLogs.clear();
    });
    
    // Event listener for account type switch button
    if (switchAccountButton) {
        switchAccountButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the account badge
            const accountBadge = document.querySelector('.account-badge .badge');
            if (!accountBadge) return;
            
            // Toggle between demo/real
            if (accountBadge.textContent === 'DEMO') {
                accountBadge.textContent = 'REAL';
                accountBadge.className = 'badge bg-danger';
                switchAccountButton.textContent = 'Switch to Demo Account';
            } else {
                accountBadge.textContent = 'DEMO';
                accountBadge.className = 'badge bg-success';
                switchAccountButton.textContent = 'Switch to Real Account';
            }
            
            // Log the account change
            const logEntry = `[${new Date().toLocaleTimeString()}] INFO: Switched to ${accountBadge.textContent} account`;
            if (!existingLogs.has(logEntry)) {
                existingLogs.add(logEntry);
                logOutput.textContent += logEntry + '\n';
                logOutput.scrollTop = logOutput.scrollHeight;
            }
        });
    }
    
    // Event listener for reset stats button
    if (resetStatsButton) {
        resetStatsButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Reset win/loss counts
            winCount = 0;
            lossCount = 0;
            
            // Update win rate display
            if (winRateValue) {
                winRateValue.textContent = '0%';
            }
            
            // Reset daily P&L display
            if (dailyPnlValue) {
                dailyPnlValue.textContent = '$0.00';
                dailyPnlValue.className = 'stat-value';
            }
            
            // Log the reset
            const logEntry = `[${new Date().toLocaleTimeString()}] INFO: Statistics reset`;
            if (!existingLogs.has(logEntry)) {
                existingLogs.add(logEntry);
                logOutput.textContent += logEntry + '\n';
                logOutput.scrollTop = logOutput.scrollHeight;
            }
        });
    }

    // Add event listener for configuration settings
    const applySettingsButton = document.getElementById('apply-settings-button');
    if (applySettingsButton) {
        applySettingsButton.addEventListener('click', async function() {
            // Get values from inputs
            const instrumentInput = document.getElementById('instrument-input');
            const durationInput = document.getElementById('duration-input');
            const durationUnitSelect = document.getElementById('duration-unit-select');
            const stakeInput = document.getElementById('stake-input');
            
            // Validate inputs
            if (!instrumentInput || !durationInput || !durationUnitSelect || !stakeInput) {
                console.error("Configuration inputs not found");
                return;
            }
            
            // Create settings object
            const settings = {
                instrument: instrumentInput.value,
                duration: parseInt(durationInput.value, 10),
                duration_unit: durationUnitSelect.value,
                stake: parseFloat(stakeInput.value)
            };
            
            // Validate settings
            let validationMessage = "";
            if (!settings.instrument) validationMessage += "Instrument cannot be empty. ";
            if (isNaN(settings.duration) || settings.duration <= 0) validationMessage += "Duration must be a positive number. ";
            if (isNaN(settings.stake) || settings.stake <= 0) validationMessage += "Stake must be a positive number. ";
            
            if (validationMessage) {
                alert("Validation error: " + validationMessage);
                return;
            }
            
            try {
                // Send settings to server
                const response = await fetch('/update_settings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(settings)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                
                const result = await response.json();
                
                // Add log entry about settings update
                const logEntry = `[${new Date().toLocaleTimeString()}] INFO: Settings updated: ${result.updated_settings ? result.updated_settings.join(', ') : 'none'}`;
                if (!existingLogs.has(logEntry)) {
                    existingLogs.add(logEntry);
                    logOutput.textContent += logEntry + '\n';
                    logOutput.scrollTop = logOutput.scrollHeight;
                }
                
                // Show notification about restart if needed
                if (result.restart_required) {
                    alert("Settings updated. Bot restart required for changes to take full effect.");
                } else {
                    alert("Settings updated successfully!");
                }
                
                // Refresh status to see updates
                fetchStatus();
                
            } catch (error) {
                console.error('Error updating settings:', error);
                alert(`Error updating settings: ${error.message}`);
            }
        });
    }

    // Initial fetch and logs setup
    fetchStatus();
    setupLogStreaming();

    // Periodic status updates
    setInterval(fetchStatus, 5000);  // Every 5 seconds
    
    // Theme switching functions
    function applyLightTheme() {
        // Update UI indicators
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        themeText.textContent = 'Dark Theme';
        
        // Apply the light theme
        htmlRoot.setAttribute('data-bs-theme', 'light');
        bootstrapTheme.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css';
        darkThemeCss.disabled = true;
        lightThemeCss.disabled = false;
        
        // Save preference
        localStorage.setItem('theme', 'light');
    }
    
    function applyDarkTheme() {
        // Update UI indicators
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
        themeText.textContent = 'Light Theme';
        
        // Apply the dark theme
        htmlRoot.setAttribute('data-bs-theme', 'dark');
        bootstrapTheme.href = 'https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css';
        darkThemeCss.disabled = false;
        lightThemeCss.disabled = true;
        
        // Save preference
        localStorage.setItem('theme', 'dark');
    }
    
    // Event listener for theme switch button
    if (switchThemeButton) {
        switchThemeButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Toggle between themes
            if (localStorage.getItem('theme') === 'light') {
                applyDarkTheme();
            } else {
                applyLightTheme();
            }
            
            // Log the theme change
            const currentTheme = localStorage.getItem('theme');
            const logEntry = `[${new Date().toLocaleTimeString()}] INFO: Switched to ${currentTheme} theme`;
            if (!existingLogs.has(logEntry)) {
                existingLogs.add(logEntry);
                logOutput.textContent += logEntry + '\n';
                logOutput.scrollTop = logOutput.scrollHeight;
            }
        });
    }

    // Start the Chart.js initialization when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize price chart if the element exists
        if (document.getElementById('priceChart')) {
            // Load Chart.js from CDN if not already loaded
            if (typeof Chart === 'undefined') {
                const script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
                script.onload = setupPriceChart;
                document.head.appendChild(script);
            } else {
                setupPriceChart();
            }
        }
    });
});
