import yfinance as yf
import pandas as pd

options_map = {

    "North America": {
        "S&P 500 (USA)": "^GSPC",
        "NASDAQ Composite (USA)": "^IXIC",
        "Dow Jones Industrial (USA)": "^DJI",
        "TSX Composite (Canada)": "^GSPTSE"
    },

    "Europe": {
        "EURO STOXX 50": "^STOXX50E",
        "FTSE 100 (UK)": "^FTSE",
        "DAX (Germany)": "^GDAXI",
        "CAC 40 (France)": "^FCHI"
    },

    "Asia": {
        "Nikkei 225 (Japan)": "^N225",
        "NIFTY 50 (India)": "^NSEI",
        "S&P BSE SENSEX (India)" : "^BSESN",
        "Hang Seng (Hong Kong)": "^HSI",
        "Shanghai Composite (China)": "000001.SS",
        "KOSPI (South Korea)": "^KS11"
    },

    "Oceania": {
        "ASX 200 (Australia)": "^AXJO",
        "NZX 50 (New Zealand)": "^NZ50"
    },

    "South America": {
        "Bovespa (Brazil)": "^BVSP",
        "MERVAL (Argentina)": "^MERV",
        "IPSA (Chile)": "^IPSA"
    },

    "Africa": {
        "FTSE/JSE All Share (South Africa)": "^JALSH",
        "EGX 30 (Egypt)": "^CASE30"
    }
}

period_options = {
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "Max": "max"
}

def get_market_data(ticker,period="max") -> pd.DataFrame:
    market=yf.Ticker(ticker).history(period=period)
    return market

def get_support_n_resistance(market_data):
    high = market_data['High'].max()
    low = market_data['Low'].min()
    return high, low

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    data = get_market_data(ticker, period="1y")
    high, low = get_support_n_resistance(data)
    print(f"Support Level: {low}, Resistance Level: {high}")