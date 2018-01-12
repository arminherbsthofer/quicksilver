from trading_interface.trading_interface import TradingInterface
from trading_interface.indicator import Indicator


class RSITrader(TradingInterface):

    def initialize(self):
        pass

    def open_position_hook(self, position):
        pass

    def close_position_hook(self, position):
        pass

    def trade(self, tohlcv):

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

