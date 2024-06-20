import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime, timedelta

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes option price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.log(-d1)
    
    return price

def fetch_nvda_options():
    # Fetch NVDA stock data
    nvda = yf.Ticker("NVDA")
    
    # Get current stock price
    current_price = nvda.history(period="1d")['Close'].iloc[-1]
    
    # Get all expiration dates
    expirations = nvda.options
    today = datetime.today()
    three_months_later = today + timedelta(days=90)
    
    # Filter expiration dates within the next 3 months
    valid_expirations = [date for date in expirations if today <= datetime.strptime(date, "%Y-%m-%d") <= three_months_later]
    
    options_data = []
    
    for exp in valid_expirations:
        # Get options chain for the expiration date
        opt = nvda.option_chain(exp)
        calls = opt.calls
        puts = opt.puts
        
        # Filter options within ±10 of the current stock price
        call_filter = (calls['strike'] >= current_price - 10) & (calls['strike'] <= current_price + 10)
        put_filter = (puts['strike'] >= current_price - 10) & (puts['strike'] <= current_price + 10)
        
        filtered_calls = calls.loc[call_filter].copy()
        filtered_puts = puts.loc[put_filter].copy()
        
        # Add expiration date to the data
        filtered_calls['expiration'] = exp
        filtered_puts['expiration'] = exp
        
        # Append to the options data list
        options_data.append(filtered_calls)
        options_data.append(filtered_puts)
    
    # Combine all options data
    combined_data = pd.concat(options_data)
    
    # Select only the specified columns
    selected_columns = ['contractSymbol', 'strike', 'lastPrice', 'volume', 'expiration']
    combined_data = combined_data[selected_columns]
    
    # Calculate time to expiration in years
    combined_data['T'] = (pd.to_datetime(combined_data['expiration']) - today).dt.days / 365.0
    
    # Add risk-free interest rate (e.g., 2%)
    r = 0.02
    
    # Add volatility (e.g., 30%)
    sigma = 0.30
    
    # Calculate Black-Scholes price for each option
    combined_data['bs'] = combined_data.apply(
        lambda row: black_scholes_price(
            S=current_price, 
            K=row['strike'], 
            T=row['T'], 
            r=r, 
            sigma=sigma, 
            option_type='call' if 'C' in row['contractSymbol'] else 'put'
        ), axis=1
    )
    
    # Round bs to 2 decimal places
    combined_data['bs'] = combined_data['bs'].round(2)
    
    # Calculate bs as a percentage of lastPrice and round to 2 decimal places
    combined_data['bs_percentage'] = ((combined_data['bs'] / combined_data['lastPrice']) * 100).round(2)
    
    # Calculate number of contracts to buy for a total price of $5000 or less
    combined_data['contracts'] = (5000 // (combined_data['lastPrice'] * 100)).astype(int)
    
    # Drop the 'T' column as it was only needed for calculation
    combined_data.drop(columns=['T'], inplace=True)
    
    # Get the current timestamp for filename
    timestamp = datetime.now().strftime("%y%m%d_%H%M")
    filename = f"option_snap_nvda_{timestamp}.csv"
    
    # Save data to CSV file
    combined_data.to_csv(filename, index=False)
    
    print(f"Options data saved to {filename}")
    
    return combined_data

def filter_and_sort_calls(data):
    # Filter for call options
    call_options = data[data['contractSymbol'].str.contains('C')]
    
    # Sort by bs_percentage in descending order
    sorted_calls = call_options.sort_values(by='bs_percentage', ascending=False)
    
    # Select only the specified columns
    selected_columns = ['contractSymbol', 'strike', 'lastPrice', 'volume', 'expiration', 'bs', 'bs_percentage', 'contracts']
    sorted_calls = sorted_calls[selected_columns]
    
    # Get the current timestamp for filename
    timestamp = datetime.now().strftime("%y%m%d_%H%M")
    filename = f"sorted_call_options_nvda_{timestamp}.csv"
    
    # Save sorted call options to CSV file
    sorted_calls.to_csv(filename, index=False)
    
    print(f"Sorted call options data saved to {filename}")

# Run the function to fetch and save NVDA options data
options_data = fetch_nvda_options()

# Run the function to filter and sort call options by bs_percentage
filter_and_sort_calls(options_data)
