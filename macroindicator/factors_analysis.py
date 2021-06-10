import pandas as pd
import pip

from datasets.datasets_base_io import load_data
import matplotlib.pyplot as plt

# loading the data
factor_returns = load_data('factor_returns.csv')
factor_returns.rename(columns={'WML': 'Momentum',
                               'SMB': 'Size',
                               'HML': 'Value',
                               'IML': 'Liquidity'},
                      inplace=True)
up_down = load_data('up_down.csv')

# join the up-down signal with factor returns
factor_up_down = up_down[['up-down']].join(factor_returns, how='inner')

# filtering by up and down scenarios
factor_up = factor_up_down.loc[factor_up_down['up-down'] == 1]
factor_down = factor_up_down.loc[factor_up_down['up-down'] == 0]

# creating df's for cumulative return of each factor in each scenario
factor_up_cum = pd.DataFrame()
factor_down_cum = pd.DataFrame()

# factor's cumulative return in up scenario
factor_up_cum['Momentum'] = (1 + factor_up.Momentum).cumprod() - 1
factor_up_cum['Size'] = (1 + factor_up.Size).cumprod() - 1
factor_up_cum['Value'] = (1 + factor_up.Value).cumprod() - 1
factor_up_cum['Liquidity'] = (1 + factor_up.Liquidity).cumprod() - 1

# factor's cumulative return in down scenario
factor_down_cum['Momentum'] = (1 + factor_down.Momentum).cumprod() - 1
factor_down_cum['Size'] = (1 + factor_down.Size).cumprod() - 1
factor_down_cum['Value'] = (1 + factor_down.Value).cumprod() - 1
factor_down_cum['Liquidity'] = (1 + factor_down.Liquidity).cumprod() - 1

# plot up scenario
fig, ax = plt.subplots(1, 1, figsize=(15, 5))
ax.plot(factor_up_cum.Momentum, color='blue')
ax.plot(factor_up_cum.Size, color='red')
ax.plot(factor_up_cum.Value, color='purple')
ax.plot(factor_up_cum.Liquidity, color='orange')
ax.legend(['Momentum', 'Size', 'Value', 'Liquidity'])
plt.show()

# plot down scenario
fig, ax = plt.subplots(1, 1, figsize=(15, 5))
ax.plot(factor_down_cum.Momentum, color='blue')
ax.plot(factor_down_cum.Size, color='red')
ax.plot(factor_down_cum.Value, color='purple')
ax.plot(factor_down_cum.Liquidity, color='orange')
ax.legend(['Momentum', 'Size', 'Value', 'Liquidity'])
plt.show()

print(1)
