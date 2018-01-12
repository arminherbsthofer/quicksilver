from trading_interface.trading_interface import TradingInterface
from trading_interface.indicator import Indicator


class SampleTemplate(TradingInterface):

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

        self.close_position(position): closes position

        self.open_positions: list that contains open positions

        self.cash: remaining cash of account
        '''
        pass
