# Trading Data Analysis Tool (Developer Draft)

## Objective
Build a Python tool to analyze trading data (OHLC, volume, spreads) and generate insights for traders.  
**Focus**: Clarify required features and their purpose for the developer.

---

## Core Features

### 1. Data Loading & Validation
- **Purpose**: Load and validate CSV/Excel files with trading data.  
- **Why Needed**:  
  - Traders need accurate, ordered time-series data for analysis.  
  - Missing/invalid data can lead to incorrect insights.  
- **Data Requirements**:  
  - Columns: `atDate`, `closing`, `bid`, `ask`, `low`, `high`, `vol`, `VWAP`, `totalRet`.  
  - Dates must be sorted (oldest to newest).  

---

### 2. Price Analysis
- **Purpose**: Track price trends and returns.  
- **Why Needed**:  
  - Traders identify momentum (e.g., rising closing prices) and performance via `totalRet`.  
- **Metrics to Calculate**:  
  - Daily returns (`(closing_t / closing_{t-1}) - 1`).  
  - Days with large price swings (>5% change).  

---

### 3. Bid-Ask Spread Analysis
- **Purpose**: Measure liquidity costs.  
- **Why Needed**:  
  - Narrow spreads = lower trading costs.  
  - Wide spreads signal illiquidity (risk for large orders).  
- **Metrics**:  
  - Average spread per day (`ask - bid`).  
  - Flag days where spread exceeds user-defined threshold.  

---

### 4. VWAP Analysis
- **Purpose**: Gauge execution quality.  
- **Why Needed**:  
  - Closing price above/below VWAP indicates buyer/seller dominance.  
- **Tasks**:  
  - Validate/calculate VWAP using `(price * volume) / cumulative volume`.  
  - Compare closing price to VWAP.  

---

### 5. Volume Analysis
- **Purpose**: Detect unusual trading activity.  
- **Why Needed**:  
  - Volume spikes often precede price breakouts or reversals.  
- **Metrics**:  
  - Flag days where volume exceeds 2x moving average (e.g., 5-day window).  

---

### 6. Risk Management Tools
- **Purpose**: Mitigate trading losses.  
- **Why Needed**:  
  - Traders need data-driven stop-loss levels.  
- **Features**:  
  - Calculate daily volatility (`high - low`).  
  - Suggest stop-loss levels based on recent lows and volatility.  

---

### 7. Visualization
- **Purpose**: Visualize trends for faster decision-making.  
- **Why Needed**:  
  - Charts help traders spot patterns (e.g., VWAP divergence).  
- **Plots to Implement**:  
  - Price + VWAP line chart.  
  - Volume bars with spike highlights.  
  - Bid-ask spread over time.  

---

### 8. Configuration (config.yaml)
- **Purpose**: Customize thresholds for alerts/analysis.  
- **Why Needed**:  
  - Traders have varying risk tolerances and strategies.  
- **Example Settings**:  
  ```yaml
  risk:
    max_volatility: 0.05  # 5%
  liquidity:
    max_spread: 0.1      # 0.1% of price
