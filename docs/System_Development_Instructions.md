---
**System Development Instructions: Deriv AI Bot - Rapid Deployment MVP**

**Core Directives:**

1.  **PRIORITY #1: SPEED VIA SIMPLICITY.** Adhere strictly to the Minimum Viable Product (MVP) scope. Defer *all* features, complex logic, or optimizations not absolutely essential for the basic, defined trading objective.
2.  **PRIORITY #2: SAFETY & STABILITY.** Implement robust error handling, comprehensive logging, and non-negotiable risk management from the outset. Extensive DEMO testing is MANDATORY before any live interaction. Live deployment starts with MINIMUM possible risk.
3.  **METHODOLOGY:** Follow the phases sequentially. Focus on establishing the core trading loop (Data -> Signal -> Risk -> Execute) reliably before expanding. Utilize standard, well-documented tools and libraries.
4.  **RISK ACKNOWLEDGEMENT:** The System Operator (Developer) acknowledges the inherent risks of automated trading. These instructions are technical guidelines; profitability is not guaranteed, and losses are possible. Compliance with Deriv.com terms and relevant regulations is mandatory.

---

**Phase 1: Planning & Strategy Definition - Instructions**

1.  **OBJECTIVE:** System MUST define ONE simple, measurable objective for the MVP (e.g., "Execute trades on EUR/USD based on MACD crossover signal filtered by RSI > 50 or < 50, running on Demo"). Record this objective.
2.  **INSTRUMENT SELECTION:** System WILL select only 1-2 highly liquid instruments known to have reliable API data feed via Deriv (e.g., EUR/USD, Volatility 75 Index). Confirm data availability in API documentation.
3.  **STRATEGY SELECTION:** System WILL implement the *simplest* viable AI/ML strategy that meets the objective.
    *   **Recommendation:** Prioritize Rule-Based + Simple ML Filter (e.g., Logistic Regression/Decision Tree on `scikit-learn`) over complex architectures for speed.
    *   Define explicit, basic entry/exit rules.
    *   Define NON-NEGOTIABLE MVP risk parameters: fixed fractional position size (e.g., 0.5% of demo balance), fixed Stop-Loss (pip or price distance), fixed Take-Profit (pip or price distance). KEEP THESE SIMPLE.
4.  **API FAMILIARIZATION:**
    *   System MUST create a Deriv DEMO account.
    *   System MUST obtain DEMO API Keys. Secure these keys locally for development (e.g., environment variables, config file - NOT committed to Git).
    *   System MUST thoroughly review Deriv API documentation focusing *only* on endpoints needed for the MVP: Authentication, Get Market Data (Candles/Ticks for selected instrument), Place Order (Market/Limit), Get Account Info (Balance), Get/Manage Open Positions.
    *   Confirm data formats, rate limits, and authentication methods.

**Phase 2: Tech Stack & Environment Setup - Instructions**

1.  **CORE TECH:**
    *   System WILL utilize Python 3.x.
    *   System WILL employ standard libraries: `requests` (for REST API calls) OR `websockets` (if Deriv offers and requires for real-time data), `pandas`, `numpy`, `scikit-learn` (for MVP ML model), `schedule` or `APScheduler` (for task timing).
    *   AVOID TensorFlow/PyTorch/complex frameworks for the initial MVP build unless the *chosen simple strategy specifically requires it and alternative simple implementations were ruled out*.
2.  **ENVIRONMENT:**
    *   System WILL set up a local development environment using `venv`.
    *   System WILL select a basic, reliable Cloud VPS provider (e.g., DigitalOcean Droplet, AWS EC2 t3.micro, Vultr VC2) for deployment. Consider server location relative to Deriv servers if ascertainable.
    *   System MUST use Git for version control from the absolute beginning. Create a repository (e.g., on GitHub/GitLab). Commit regularly with clear messages. Ensure API keys and sensitive configs are in `.gitignore`.
3.  **DERIV PLATFORM TOOLS:** Evaluate Deriv's DBot/Binary Bot *only* if the complexity matches their visual builder AND you choose to forego custom AI/Python flexibility for the MVP. Otherwise, stick to the API route as planned.

**Phase 3: Core Development - Instructions**

1.  **API WRAPPER:** System WILL build a dedicated module (`deriv_api.py` or similar) containing functions for ALL interactions with the Deriv API.
    *   Mandatory functions: `connect_api`, `get_price_data`, `place_trade`, `get_open_trades`, `close_trade`, `get_balance`.
    *   Implement basic retry logic for transient network errors.
    *   Log EVERY API call (request parameters) and response (or error). Use Python's `logging` module.
2.  **DATA HANDLING:** System WILL implement functions to:
    *   Fetch historical data required ONLY for training the *simple* ML model (if applicable), possibly run offline once.
    *   Fetch near-real-time market data (e.g., latest candles or ticks) as required by the strategy. Handle data parsing into usable formats (e.g., Pandas DataFrame).
3.  **SIGNAL GENERATION:** System WILL implement the logic defined in Phase 1.
    *   If ML is used: Load the pre-trained `scikit-learn` model. Create a function `generate_signal(current_data)` that inputs market data and outputs a clear signal (e.g., BUY, SELL, HOLD).
    *   Keep calculations efficient.
4.  **TRADING LOGIC:** System WILL implement the main execution loop:
    *   `Fetch Data` -> `Generate Signal` -> `Apply Risk Rules` -> `Execute Trade (if signal valid AND risk rules pass)`.
    *   This loop MUST be triggered by the chosen scheduler (`schedule`/`APScheduler`) at the defined frequency (e.g., every 1 minute, every 5 minutes).
5.  **RISK MANAGEMENT:** System MUST embed the following as HARD-CODED checks *before* `place_trade` is ever called:
    *   Check if calculated position size exceeds the defined maximum.
    *   Ensure every trade order includes the pre-defined MANDATORY Stop-Loss.
    *   Check if the number of open trades is less than the maximum allowed (start with 1).
    *   Perform a basic balance check (optional for MVP, but good practice). Log risk rule checks.
6.  **LOGGING:** System MUST implement COMPREHENSIVE logging to a file:
    *   Bot startup/shutdown.
    *   Scheduled task execution.
    *   Data fetching success/failure.
    *   Signal generation results.
    *   Risk rule check outcomes (pass/fail).
    *   Order placement attempts (including parameters).
    *   Order confirmations/rejections from API.
    *   Any errors or exceptions encountered (with tracebacks).
    *   Account balance updates (periodically).

**Phase 4: Testing - Instructions**

1.  **BACKTESTING:** System WILL perform *simplified* backtesting only if the strategy allows and data is easily available. GOAL: Rough validation, not perfection. DO NOT spend significant time here for MVP.
2.  **UNIT TESTING:** System MUST create basic unit tests (using `pytest` or `unittest`) for critical, non-API-dependent functions like signal generation logic and risk rule calculations.
3.  **FORWARD TESTING (CRITICAL):**
    *   System MUST deploy the bot code to the chosen VPS.
    *   System MUST configure the bot to use DEMO API Keys *ONLY*.
    *   System MUST run the bot continuously on the DEMO account for a MINIMUM period defined (e.g., 1-2 weeks) to cover various market conditions.
    *   System Operator MUST actively monitor logs, VPS resource usage (CPU/RAM), and trade execution within the Deriv Demo platform.
    *   Verify: Orders placed correctly? SL/TP working? Error handling functioning? Bot stable over time?
    *   DO NOT PROCEED TO PHASE 5 UNTIL DEMO PERFORMANCE IS STABLE AND AS EXPECTED.

**Phase 5: Deployment (MVP Live - Minimal Risk) - Instructions**

1.  **GO/NO-GO:** System proceeds ONLY IF Phase 4 Demo Testing was satisfactory and stable.
2.  **PRE-FLIGHT CHECKS:**
    *   System MUST ensure LIVE API keys are secured correctly on the VPS (e.g., environment variables). DOUBLE-CHECK that no keys are in code/Git.
    *   Verify logging configuration directs to persistent files on the server.
    *   Verify bot process runs reliably (e.g., using `systemd` or `supervisor` on Linux).
3.  **INITIAL LIVE DEPLOYMENT:**
    *   System WILL stop the demo bot, update configuration with LIVE API keys.
    *   System WILL configure the bot to use the ABSOLUTE MINIMUM possible trade size allowed by Deriv for the chosen instrument.
    *   System MAY initially reduce execution frequency (if applicable).
    *   System WILL start the live bot.
    *   GOAL: Verify technical function in the live environment (latency, fills), NOT immediate profit.

**Phase 6: Monitoring & Iteration - Instructions**

1.  **INTENSE MONITORING:** System Operator MUST monitor the live MVP bot rigorously:
    *   Check logs frequently for errors.
    *   Monitor VPS status (uptime, CPU, RAM).
    *   Observe live trade execution and P/L in the Deriv platform.
    *   Stay informed about Deriv platform status/maintenance.
2.  **ITERATION:** System development is continuous:
    *   Address critical bugs immediately.
    *   Refine strategy or risk parameters ONLY after careful observation and based on performance data (demo or minimal-risk live). Make incremental changes.
    *   Consider GRADUALLY increasing trade size ONLY after consistent, stable performance and if aligned with risk tolerance.
    *   Defer adding new features/complexity until the MVP core is proven robust. Document all changes via Git.
---