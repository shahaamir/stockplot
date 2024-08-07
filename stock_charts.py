import yfinance as yf
import plotly.graph_objects as go
import plotly.subplots as sp

# List of stock symbols
stocks = ['RELIANCE.NS', 'INFY.NS', 'TCS.NS', 'ITC.NS', 'GICRE.NS', 'ICICIBANK.NS', 'AXISBANK.NS']

# Fetch data for the past 5 years
data = {stock: yf.download(stock, period="5y") for stock in stocks}

# Function to calculate EMA
def calculate_ema(data, span):
    return data.ewm(span=span, adjust=False).mean()

# Create subplots for each stock
fig = sp.make_subplots(rows=len(stocks), cols=1, subplot_titles=stocks)

# Add candlestick charts and EMAs to each subplot
for i, stock in enumerate(stocks):
    stock_data = data[stock]
    stock_data['50 EMA'] = calculate_ema(stock_data['Close'], 50)
    stock_data['200 EMA'] = calculate_ema(stock_data['Close'], 200)
    
    # Add Candlestick trace
    candle_stick = go.Candlestick(x=stock_data.index.date,
                                 open=stock_data['Open'],
                                 high=stock_data['High'],
                                 low=stock_data['Low'],
                                 close=stock_data['Close'],
                                 name=f'{stock} Candlestick')
    fig.add_trace(candle_stick, row=i+1, col=1)
   
    # Add 50 EMA trace
    #print(stock_data.index)
    ema50 = go.Scatter(x=stock_data.index.date, y=stock_data['50 EMA'], line=dict(color='blue', width=1), name='50 EMA')
    fig.append_trace(ema50, row=i+1, col=1)
    
    # Add 200 EMA trace
    ema200 = go.Scatter(x=stock_data.index.date, y=stock_data['200 EMA'], line=dict(color='red', width=1), name='200 EMA')
    fig.append_trace(ema200, row=i+1, col=1)

    # Update each subplot's x-axis and y-axis
    fig.update_xaxes(rangeslider_visible=False, tickformat="%d %b %Y", row=i+1, col=1, showspikes=True, spikesnap='cursor', spikemode='across', spikedash='solid')
    fig.update_yaxes(fixedrange=False, row=i+1, col=1, showspikes=True, spikesnap='cursor', spikemode='across', spikedash='solid')

# Update layout
fig.update_layout(height=500*len(stocks), title_text="Candlestick Charts with 50 EMA and 200 EMA for Selected Stocks Over the Last 5 Years",
                  showlegend=True, dragmode='pan')  # Show legend for clarity

# Display the figure
fig.show()
