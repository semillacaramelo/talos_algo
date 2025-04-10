# Updated README

## AI-Automated Trading Bot on Deriv.com

**Disclaimer:**
Trading involves significant risk, and automated trading, especially with AI, does not guarantee profits. Losses can exceed deposits. This project is for informational purposes; ensure you understand the risks, Deriv's terms, and relevant regulations before proceeding. Start with thorough testing on a demo account and use real money cautiously only if you fully accept the risks.

### Project Structure

```
/workspaces/talos_algo
├── README.md
├── config/
│   ├── settings.py
│   └── secrets.env
├── docs/
│   ├── project_proposal.md
│   ├── Rapid_Deployment_Project_Plan.md
│   ├── System_Development_Instructions.md
│   └── API_Documentation.md
├── logs/
│   └── bot.log
├── src/
│   ├── api/
│   │   ├── deriv_api_handler.py
│   │   └── __init__.py
│   ├── data/
│   │   ├── data_handler.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── signal_model.py
│   │   └── __init__.py
│   ├── trading/
│   │   ├── trading_logic.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── logger.py
│   │   └── __init__.py
│   └── main.py
├── tests/
│   ├── test_api/
│   │   ├── test_deriv_api.py
│   │   └── __init__.py
│   ├── test_data/
│   │   ├── test_data_handler.py
│   │   └── __init__.py
│   ├── test_models/
│   │   ├── test_signal_model.py
│   │   └── __init__.py
│   ├── test_trading/
│   │   ├── test_trading_logic.py
│   │   └── __init__.py
│   └── conftest.py
└── requirements.txt
```

### Key Features
- Modular design for scalability and maintainability.
- Comprehensive logging and error handling.
- Focus on safety and simplicity for rapid deployment.

### Getting Started
1. Clone the repository.
2. Set up a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   **Note:** If you encounter dependency conflicts during installation, particularly with numpy versions, try these solutions:
   - Use the updated requirements.txt which properly manages package version conflicts
   - If issues persist with python-deriv-api installation, install it directly:
     ```bash
     pip install git+https://github.com/deriv-com/python-deriv-api.git@7e8dd0f0920d4eac0fb904891e4005178a30ee19
     ```

3. Configure `config/settings.py` and `config/secrets.env` with your settings and API keys.
4. Run the bot:
   ```bash
   python src/main.py
   ```

### Web Interface
The project includes a Flask-based web dashboard for:
- Starting and stopping the trading bot
- Monitoring bot status and active trades 
- Viewing account balance and performance metrics
- Accessing real-time logs
- Configuring settings

To start the web interface:
```bash
python app.py
```
Then navigate to http://localhost:5000 in your browser.