import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("processed_stock_data.csv")

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Fill missing values 
df = df.fillna(method='bfill').dropna()


# Buy when short MA (MA_7) > long MA (MA_30)
df['Signal'] = 0
df.loc[df['MA_7'] > df['MA_30'], 'Signal'] = 1  # Signal for buy

# Use previous day's signal to simulate real trading
df['Strategy Return'] = df['Signal'].shift(1) * df['Daily Return']

# Cumulative return of the strategy
df['Cumulative Strategy Return'] = (1 + df['Strategy Return']).cumprod()

# Plot Strategy vs Buy & Hold

plt.figure(figsize=(14, 6))
plt.plot(df.index, df['Cumulative Return'], label='Buy & Hold', linewidth=2)
plt.plot(df.index, df['Cumulative Strategy Return'], label='Strategy', linestyle='--', linewidth=2)
plt.title("Cumulative Returns: Moving Average Crossover Strategy vs Buy & Hold")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (Growth of $1)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Total Return
total_return = df['Strategy Return'].sum()
buy_hold_return = df['Daily Return'].sum()

# Annualized Return (assuming 252 trading days per year)
annualized_strategy_return = np.mean(df['Strategy Return']) * 252
annualized_buy_hold_return = np.mean(df['Daily Return']) * 252

# Volatility 
annualized_strategy_volatility = np.std(df['Strategy Return']) * np.sqrt(252)
annualized_buy_hold_volatility = np.std(df['Daily Return']) * np.sqrt(252)

# Sharpe Ratio 
sharpe_strategy = annualized_strategy_return / annualized_strategy_volatility
sharpe_buy_hold = annualized_buy_hold_return / annualized_buy_hold_volatility

print("----- Strategy Performance Metrics -----")
print(f"Total Strategy Return: {total_return:.2%}")
print(f"Annualized Strategy Return: {annualized_strategy_return:.2%}")
print(f"Annualized Strategy Volatility: {annualized_strategy_volatility:.2%}")
print(f"Sharpe Ratio (Strategy): {sharpe_strategy:.2f}")
print()
print("----- Buy & Hold Performance Metrics -----")
print(f"Total Buy & Hold Return: {buy_hold_return:.2%}")
print(f"Annualized Buy & Hold Return: {annualized_buy_hold_return:.2%}")
print(f"Annualized Buy & Hold Volatility: {annualized_buy_hold_volatility:.2%}")
print(f"Sharpe Ratio (Buy & Hold): {sharpe_buy_hold:.2f}")