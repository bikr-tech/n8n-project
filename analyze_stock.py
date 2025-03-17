import yfinance as yf
import pandas as pd
import numpy as np
import json
import argparse

# Fetch stock data
parser = argparse.ArgumentParser(description="Analyze stock data")
parser.add_argument("symbol", help="Stock symbol to analyze")
args = parser.parse_args()
ticker = args.symbol
data = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True)

# Ensure that we have enough data for RSI (at least 14 days)
if len(data) >= 14:
    # RSI Calculation
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    # MACD Calculation
    short_ema = data["Close"].ewm(span=12, adjust=False).mean()
    long_ema = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD"] = short_ema - long_ema
    data["Signal Line"] = data["MACD"].ewm(span=9, adjust=False).mean()

    # 50-day and 200-day Moving Averages
    data["50_MA"] = data["Close"].rolling(window=50).mean()
    data["200_MA"] = data["Close"].rolling(window=200).mean()

    # Volume Analysis
    data["Volume_MA"] = data["Volume"].rolling(window=20).mean()

    # Output the latest values
    latest_rsi = (
        round(data["RSI"].iloc[-1], 2) if not pd.isna(data["RSI"].iloc[-1]) else "N/A"
    )
    latest_macd = (
        round(data["MACD"].iloc[-1], 2) if not pd.isna(data["MACD"].iloc[-1]) else "N/A"
    )
    latest_signal = (
        round(data["Signal Line"].iloc[-1], 2)
        if not pd.isna(data["Signal Line"].iloc[-1])
        else "N/A"
    )
    latest_50_ma = (
        round(data["50_MA"].iloc[-1], 2)
        if not pd.isna(data["50_MA"].iloc[-1])
        else "N/A"
    )
    latest_200_ma = (
        round(data["200_MA"].iloc[-1], 2)
        if not pd.isna(data["200_MA"].iloc[-1])
        else "N/A"
    )
    latest_volume_ma = (
        round(data["Volume_MA"].iloc[-1], 2)
        if not pd.isna(data["Volume_MA"].iloc[-1])
        else "N/A"
    )

    # Generate dynamic HTML content
    html_output = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            h1 {{
                color: #4CAF50;
            }}
            h2 {{
                color: #333;
            }}
            .analysis-section {{
                margin-bottom: 20px;
            }}
            .section-header {{
                font-weight: bold;
                color: #333;
            }}
            .recommendation {{
                margin-top: 30px;
                font-size: 18px;
                font-weight: bold;
            }}
            .positive {{
                color: green;
            }}
            .negative {{
                color: red;
            }}
            .neutral {{
                color: orange;
            }}
        </style>
    </head>
    <body>
    
    <h1>{ticker} - Stock Analysis Report</h1>
    
    <div class="analysis-section">
        <h2>1. RSI Analysis</h2>
        <p class="section-header">RSI (Relative Strength Index): {latest_rsi}</p>
        <p><strong>Interpretation:</strong> If the RSI is above 70, it suggests that the stock may be in an overbought environment, which could indicate potential selling opportunities.</p>
    </div>

    <div class="analysis-section">
        <h2>2. MACD Analysis</h2>
        <p class="section-header">MACD: {latest_macd}</p>
        <p><strong>Interpretation:</strong> A positive MACD signal combined with a rising MACD line suggests that the stock may be in an upward trend, which could support buying.</p>
    </div>

    <div class="analysis-section">
        <h2>3. Signal Analysis</h2>
        <p class="section-header">Signal: {latest_signal}</p>
        <p><strong>Interpretation:</strong> If the MACD Signal crosses above/below the MACD Line, it can indicate a potential buy/sell signal, depending on the context (bullish or bearish).</p>
    </div>

    <div class="analysis-section">
        <h2>4. Moving Averages Analysis</h2>
        <p class="section-header">50-day Moving Average: {latest_50_ma}</p>
        <p>If the price breaks below {latest_50_ma}, buying could make sense after confirming upward momentum.</p>
        <p><strong>Interpretation:</strong> A rising 50-day MA indicates bullish strength.</p>

        <p class="section-header">200-day Moving Average: {latest_200_ma}</p>
        <p>If the price breaks below {latest_200_ma}, selling could make sense after confirming potential upside.</p>
        <p><strong>Interpretation:</strong> A falling 200-day MA indicates bearish strength.</p>
    </div>

    <div class="analysis-section">
        <h2>5. Volume Analysis</h2>
        <p class="section-header">Volume (20-day Moving Average): {latest_volume_ma}</p>
        <p><strong>Interpretation:</strong> High volume can indicate strong demand and potential price gains, making buying or even selling more attractive.</p>
    </div>

    <h2>Conclusion</h2>
    <p>Based on the analysis of these technical indicators:</p>
    <ol>
        <li>If the RSI is above 70, it may indicate overbought conditions, and you might consider selling if the price drops below {latest_50_ma}.</li>
        <li>A rising MACD Signal combined with a rising MACD Line could indicate bullish momentum and support for buying.</li>
        <li>A falling 200-day MA at {latest_200_ma} may offer an upside potential if the price breaks below that level after crossing above it.</li>
    </ol>

    <h2>Final Recommendation</h2>
    <p class="recommendation">
        <span class="positive">Buy:</span> If the stock is trending upward with high volume, rising MACD Line, and a rising 200-day MA.<br>
        <span class="negative">Sell:</span> If the RSI is above 70, and the price breaks below {latest_50_ma} after being crossed above or below.<br>
        <span class="neutral">Hold:</span> If neither strong momentum nor significant overshot occurs.
    </p>

    </body>
    </html>
    """

    print(html_output)

else:
    print("Error: Insufficient data to calculate indicators")
