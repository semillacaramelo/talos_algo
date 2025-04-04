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
        } else if (status === 'Stopping' || status === 'Starting bot...') {
            icon.classList.add('fa-sync-alt');
            icon.style.animation = 'fa-spin 2s infinite linear';
        } else if (status === 'Error') {
            icon.classList.add('fa-exclamation-circle');
        } else {
            icon.classList.add('fa-info-circle');
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
        instrumentValue.textContent = config.instrument || 'N/A';
        durationValue.textContent = config.duration || 'N/A';
        stakeValue.textContent = config.stake || 'N/A';
        
        // Optional value update if the field exists
        if (maxTradesValue) {
            maxTradesValue.textContent = config.max_concurrent_trades || '3';
        }
    }

    // Update live state display
    function updateStateDisplay(balance, activeTrades, lastPrice, lastSignal, uptime, featureCount, lastTrade) {
        if (balanceValue) balanceValue.textContent = balance || 'N/A';
        if (activeTradesValue) activeTradesValue.textContent = activeTrades || '0';
        if (lastPriceValue) lastPriceValue.textContent = lastPrice || 'N/A';
        
        // Update last signal with appropriate styling
        if (lastSignalValue) {
            lastSignalValue.textContent = lastSignal || 'N/A';
            lastSignalValue.className = 'badge';
            
            if (lastSignal === 'BUY') {
                lastSignalValue.classList.add('bg-success');
            } else if (lastSignal === 'SELL') {
                lastSignalValue.classList.add('bg-danger');
            } else {
                lastSignalValue.classList.add('bg-secondary');
            }
        }
        
        if (uptimeValue) uptimeValue.textContent = uptime || 'N/A';
        if (featureCountValue) featureCountValue.textContent = featureCount || 'N/A';
        if (lastTradeValue) lastTradeValue.textContent = lastTrade || 'N/A';
        
        // Calculate win rate if we have the data
        if (winRateValue) {
            const totalTrades = winCount + lossCount;
            if (totalTrades > 0) {
                const rate = Math.floor((winCount / totalTrades) * 100);
                winRateValue.textContent = `${rate}%`;
            } else {
                winRateValue.textContent = '0%';
            }
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

    // Fetch and update status
    async function fetchStatus() {
        const data = await fetchFromAPI('/get_status');
        if (data) {
            updateStatusDisplay(data.status);
            updateConfigDisplay(data.config);
            updateStateDisplay(
                data.balance, 
                data.active_trades, 
                data.last_price, 
                data.last_signal,
                data.uptime,
                data.feature_count,
                data.last_trade
            );
            
            // Update trades table if we have trade data
            if (data.trades) {
                currentTrades = data.trades;
                updateTradesTable(data.trades);
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

    // Initial fetch and logs setup
    fetchStatus();
    fetchLogs();

    // Periodic status updates
    setInterval(fetchStatus, 5000);  // Every 5 seconds
});
