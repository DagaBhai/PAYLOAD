# QuantVista 📊

A comprehensive machine learning platform for analyzing global financial markets, computing quantitative metrics, and forecasting price trends using rigorous analytical methods.

## 🎯 Overview

**BEST QUANTIFIER** is a Streamlit-based application that enables users to:

- **Analyze Market Data** - Visualize price movements across 50+ global indices (S&P 500, Sensex, NIKKEI 225, etc.)
- **Compute Quantitative Metrics** - Calculate 14 advanced financial indicators with AI-powered interpretation
- **Compare Markets** - Perform dual-axis comparisons across different exchanges and currencies
- **Forecast Prices** - Use LSTM neural networks for short-term market predictions (7-14 days)
- **Consult AI Expert** - Interactive chatbot powered by Gemini 2.5 Flash for market insights

---

## 🏗️ Project Structure

```
payload/
├── App.py                          # Main Streamlit application & navigation
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── pages/
│   ├── market_page.py             # Market chart visualization & selection
│   ├── market_compare_page.py      # Dual-market comparison dashboard
│   ├── metrics_page.py            # Quantitative metrics computation & visualization
│   ├── ask_ai_page.py             # AI chatbot for metric interpretation
│   └── forecasting_page.py        # LSTM-based price forecasting
└── tools/
    ├── market.py                  # Data fetching (14 market categories, 50+ indices)
    ├── metrics.py                 # 14 quantitative metrics implementations
    ├── Interpretation.py          # Metric interpretation rules & logic
    └── lstm_model.py              # LSTM architecture & forecasting pipeline
```

---

## 📊 Features & Deliverables

### A. Data Analysis & Feature Engineering

All metrics are computed from real-time financial data via **yfinance**:

| Metric | Category | Description |
|--------|----------|-------------|
| **Log Return** | Returns | Daily logarithmic returns for price changes |
| **Support & Resistance** | Levels | 20-period rolling min/max for price targets |
| **Rolling Extreme** | Momentum | Normalized position within support/resistance |
| **Rate of Change (Daily/Weekly/Monthly)** | Momentum | Percentage change across 1, 5, 21-day periods |
| **Volatility** | Risk | 20-period rolling standard deviation of returns |
| **Volatility Ratio** | Risk | Short (20) vs Long (50) window volatility |
| **Moving Average Distance** | Trend | Ratio of price deviation from MA bands |
| **Moving Average Slope** | Trend | First derivative of 20-period moving average |
| **MACD (3 variants)** | Momentum | Exponential moving average convergence divergence |

**Implementation**: See `tools/metrics.py`

### B. Modeling & Insights

#### Machine Learning Models

1. **LSTM Neural Network** (`tools/lstm_model.py`)
   - Architecture: LSTM(64) → Dense(32, relu) → Dense(32, relu) → Dense(1)
   - Training: 100 epochs with Adam optimizer (lr=0.001)
   - Features: 3-day windowed lookback for sequential prediction
   - **Assumption**: Market exhibits temporal dependencies capturable by LSTM cells
   - **Scope**: 7-14 day forecasts only (short-term, educational use)

#### Interpretation Engine

- **Rule-based system** (`tools/Interpretation.py`) with 40+ interpretive statements
- Classifies each metric into regimes (e.g., "bullish", "volatile", "expanding")
- Context-aware language explaining market implications
- **Example**: High volatility ratio → "Volatility expansion suggests regime transition"

### C. Visualization & Reporting

**Interactive Dashboards** via Streamlit:

1. **Market Chart Page** (`pages/market_page.py`)
   - Multi-market dashboard with add/remove functionality
   - Historical price visualization (1mo - max data)
   - Quick access to quantitative analysis

2. **Market Comparison** (`pages/market_compare_page.py`)
   - Dual-axis Plotly charts for currency-aware comparisons
   - Side-by-side analysis of different indices/currencies
   - Real-time currency detection via yfinance

3. **Metrics Dashboard** (`pages/metrics_page.py`)
   - 14 customizable technical indicators
   - Automated interpretation for each metric
   - Interactive selection with line charts
   - AI-powered deep-dive option

4. **AI Chatbot** (`pages/ask_ai_page.py`)
   - Gemini 2.5 Flash with Google Search integration
   - Context-aware: receives selected metrics as background
   - Chat history persistence within session

5. **Forecasting Dashboard** (`pages/forecasting_page.py`)
   - LSTM predictions with user-defined horizons (7-14 days)
   - Disclaimer on volatility & educational scope
   - Visual overlay of historical + predicted prices

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip package manager
- Internet connection (for yfinance & Google Gemini API)

### Installation (4 Steps)

#### Step 1: Clone & Navigate
```bash
cd c:\Users\Yash\OneDrive\Desktop\payload
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```
Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

#### Step 4: Run Application
```bash
streamlit run App.py
```
Open browser → `http://localhost:8501`

---

## 📈 Usage Guide

### Step 1: Select & Visualize Market
1. Navigate to **Market Chart** (📊)
2. Select category (North America, Europe, Asia, etc.)
3. Choose market index (S&P 500, Sensex, etc.)
4. Set time period (1mo - max)
5. Click "Add to Dashboard"

### Step 2: Compute Metrics
1. Click **View Quant Metrics** on market chart
2. Multi-select desired metrics from 14 options
3. View dataframe & automated interpretations
4. Graphs with regime classifications

### Step 3: Compare Markets
1. Go to **Market Comparision** (🔍)
2. Select two different indices
3. Click **Comparison Graphs** for dual-axis chart
4. Compare trends across currencies

### Step 4: Forecast Future Prices
1. Navigate to **Forecasting** (🔮)
2. Select market & set horizon (7-14 days)
3. Click **Run Forecast**
4. View LSTM predictions overlaid on historical data

### Step 5: Ask AI Expert
1. Go to **Metrics** (📈) → select metrics → "Interpret Using Our AI"
2. Or directly to **Stock Market Expert Chatbot** (🤖)
3. Ask questions about market data & get AI-powered responses

---
