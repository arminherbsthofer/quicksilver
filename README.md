# Quicksilver

Quicksilver is a library for backtesting and live trading. It is easily extendable and allows for a seemless transition between backtesting and live trading.
It lets you focus on algorithm development and eliminates the risk of accidentally feeding future data into your models.

### Prerequisites

Quicksilver requires some scientific python packages for numerical computations and visualization such as numpy, pandas and matplotlib.
Installing anaconda should have you covered. Simply download this repository and copy it into your project.

## Getting Started

First you have to write some trading logic by extending the trading interface.
Below is an example of an algorithm using the RSI indicator for trading.
Every Quicksilver algorithm must overide the ```initialize``` method and the ```trade``` method. ```initialize``` is called only once at the beginning of trading and can be used to setup global variables, load machine learning
classifiers, etc. ```trade``` is called for every tick of the asset you are trading. The timeframe (1m, 30m, 1h, ...) depends on the data you feed in the main loop.
```open_position_hook``` and ```close_position_hook``` are optional. They are called upon every open and close position event and can be used to execute the order at some exchange or send notifications to your inbox for example.

```python

from quicksilver.trading_interface.trading_interface import TradingInterface
from quicksilver.trading_interface.indicator import Indicator


class RSITrader(TradingInterface):

    def initialize(self):
        pass

    def open_position_hook(self, position):
        pass

    def close_position_hook(self, position):
        pass

    def trade(self, tohlcv):
        '''
        tohlcv: dictionary indexed by symbol names, each symbol holds the current value
                of timestamp, open, high, low, close and volume for the current timestep
                e.g. tohlcv['BTC']['Close']

        self.history: contains complete history, same structure as tohlcv
                      e.g. to get last 10 close values of BTC self.history['BTC']['Close'][-10:]

        self.open_position(tohlcv, symbol, quantity, action, stop_loss, take_profit): opens position 
                      if no stop loss or take profit is given, you have to close the position manually 
                      according to your algorithm logic

        self.close_position(position): closes position

        self.open_positions: list that contains open positions

        self.cash: remaining cash of account

        for more options consult the TradingInterface source code
        '''
        
        indicator = Indicator()
        rsi = indicator.RSI(self.history['BTC'], 60)

        price = tohlcv['BTC']['Close']

        # place sltp according to current market price
        sl = price * 0.015
        tp = price * 0.025

        # always trade only 0.1% of the account
        quantity = (self.cash * 0.01) / price

        # technical signal
        long_signal = (rsi[-2] < 30) and (rsi[-1] >= 30)
        short_signal = (rsi[-2] > 70) and (rsi[-1] <= 70)

        if short_signal:
            self.open_position(tohlcv, 'BTC', quantity, action='short', stop_loss=price+sl, take_profit=price-tp)
        if long_signal:
            self.open_position(tohlcv, 'BTC', quantity, action='long', stop_loss=price-sl, take_profit=price+tp)

```

Then you can run this algorithm in the trading loop like so:

```python

import pandas as pd

from quicksilver.visualization.trading_visualizer import TradingVisualizer

data = pd.read_csv('tohlcv.csv')
data = data.loc['2016-06-01':'2017-03-01']

rsi_trader = RSITrader(cash=1000000, verbose=0)

counter = 0
for index, row in data.iterrows():

    # build tohlcv object
    tohlcv = {'BTC':
        {
            'Timestamp': index.value / 10 ** 9,
            'Open': row.Open,
            'High': row.High,
            'Low': row.Low,
            'Close': row.Close,
            'Volume': row.Volume
        }
    }

    rsi_trader.tick(tohlcv)

    # display progress
    if counter % 500 == 0:
        print(round(counter / len(data) * 100, 2), '%')
    counter += 1

trading_visualizer = TradingVisualizer(rsi_trader)
trading_visualizer.visualize('BTC')

```

Simply look at the source code of the TradingInterface to see which parameters are tracked by default like portfolio value development, cash development, etc.
You can also track custom quantities with the record function. Above we also imported a rudimentary visualizer that displays interesting quantities at the end of a trading epoch.

## Contributing

Contributions and testing are very welcome.

## Authors

* **Armin Herbsthofer** 2018
