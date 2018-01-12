import numpy as np

from trading_interface.position import Position


class TradingInterface:
    def __init__(self, cash, verbose=0):

        # live data objects
        self.cash = np.float64(cash)
        self.portfolio_value = np.float64(cash)
        self.position_value = np.float64(0)
        self.open_positions = []

        # storage data objects
        self.history = {}
        self.cash_history = []
        self.portfolio_value_history = []
        self.position_value_history = []
        self.marked_for_closing = []
        self.closed_positions = []
        self.record = {}

        # flags
        self.verbose = verbose

        # call initialize hook
        self.initialize()

    def record(self, key, value):
        '''
            allows tracking arbitrary values
        '''
        if key in self.record:
            self.record[key].append(value)
        else:
            self.record[key] = [value]

    def open_position(self, tohlcv, symbol, quantity, action='long', stop_loss=None, take_profit=None):
        '''
            opens a long or short position
        '''
        timestamp = tohlcv[symbol]['Timestamp']
        price = tohlcv[symbol]['Close']

        if self.cash >= quantity * price:

            # create position
            position = Position(symbol, quantity, price, timestamp, action, 'open', stop_loss, take_profit)
            self.open_positions.append(position)
            self.cash -= quantity * price
            self.position_value += quantity * price

            try:
                self.open_position_hook(position)
            except Exception:
                if self.verbose:
                    print('following position not opened at exchange: ')

            if self.verbose:
                print(str(timestamp), ': ordered ', str(quantity), ' ', symbol, ' at: ', str(price))
        else:
            if self.verbose:
                print(str(timestamp), ': order of ', str(quantity), ' ', symbol, ' at ', str(price),
                      'failed: insufficient funds')

    def close_position(self, position, tohlcv):
        '''
            closes a position
        '''
        if position.status == 'closed':
            if self.verbose:
                print('position already closed')

        price = tohlcv[position.symbol]['Close']

        if position.action == 'long':
            change = price * position.quantity
            self.cash += change
            self.position_value -= change

        if position.action == 'short':
            change = (2 * position.price - price) * position.quantity
            self.cash += change
            self.position_value -= change

        position.status = 'closed'
        self.marked_for_closing.append(position)

        try:
            self.close_position_hook(position)
        except Exception:
            if self.verbose:
                print('following position not closed at exchange: ')

    def update_closed_positions(self):
        '''
            moves closed positions to correct lists
        '''
        for position in self.marked_for_closing:
            self.closed_positions.append(position)
            self.open_positions.remove(position)

        self.marked_for_closing = []

    def update_portfolio_and_position_value(self, tohlcv):
        '''
            updates portfolio and position value according to new market prices
        '''
        position_value = 0

        for position in self.open_positions:
            if position.action == 'long':
                position_value += tohlcv[position.symbol]['Close'] * position.quantity
            if position.action == 'short':
                position_value += (2 * position.price - tohlcv[position.symbol]['Close']) * position.quantity

        self.position_value = position_value
        self.portfolio_value = self.cash + position_value

    def check_open_positions(self, tohlcv):
        '''
            checks stop loss and take profit levels for all open positions and closes them if neccessary
        '''
        for position in self.open_positions:

            if position.status == 'open':
                price = tohlcv[position.symbol]['Close']

                if position.stop_loss:
                    if position.action == 'long' and price < position.stop_loss:
                        self.close_position(position, tohlcv)
                    if position.action == 'short' and price > position.stop_loss:
                        self.close_position(position, tohlcv)

                if position.take_profit:
                    if position.action == 'long' and price > position.take_profit:
                        self.close_position(position, tohlcv)
                    if position.action == 'short' and price < position.take_profit:
                        self.close_position(position, tohlcv)

    def save_history(self, tohlcv):
        '''
            saves current tohlcv in history for easy access in trading algorithm
        '''
        for symbol in tohlcv:
            if symbol in self.history:
                self.history[symbol]['Timestamp'].append(tohlcv[symbol]['Timestamp'])
                self.history[symbol]['Open'].append(tohlcv[symbol]['Open'])
                self.history[symbol]['High'].append(tohlcv[symbol]['High'])
                self.history[symbol]['Low'].append(tohlcv[symbol]['Low'])
                self.history[symbol]['Close'].append(tohlcv[symbol]['Close'])
                self.history[symbol]['Volume'].append(tohlcv[symbol]['Volume'])
            else:
                self.history[symbol] = {
                    'Timestamp': [tohlcv[symbol]['Timestamp']],
                    'Open': [tohlcv[symbol]['Open']],
                    'High': [tohlcv[symbol]['High']],
                    'Low': [tohlcv[symbol]['Low']],
                    'Close': [tohlcv[symbol]['Close']],
                    'Volume': [tohlcv[symbol]['Volume']]
                }

    def tick(self, tohlcv):
        '''
            tohlcv: dictionary containing an entry for each symbol. each entry is itself a dictionary containing
                    timestamp, open, high, low, close and volume
        '''

        # update portfolio value
        self.update_portfolio_and_position_value(tohlcv)

        # store tohlcv object, cash, portfolio and position value in history
        self.save_history(tohlcv)
        self.cash_history.append(self.cash)
        self.portfolio_value_history.append(self.portfolio_value)
        self.position_value_history.append(self.position_value)

        # check if open positions need to be closed according to stop loss and take profit
        self.check_open_positions(tohlcv)

        # move positions marked for closing to the closed positions list and remove it from open positions
        self.update_closed_positions()

        self.trade(tohlcv)

    def trade(self, tohlcv):
        '''
            contains trading logic
            must be overridden by algorithm implementations
        '''
        raise NotImplementedError

    def initialize(self):
        '''
            is called at the end if the __init__ method
            must be overridden by algorithm implementation
            can be used to setup global variables needed for the algorithm
        '''
        raise NotImplementedError

    def open_position_hook(self, position):
        '''
            is called upon opening an order
            can be overridden by algorithm implementation and can call specific api endpoints of an exchange
        '''
        pass

    def close_position_hook(self, position):
        '''
            is called upon closing an order
            can be overridden by algorithm implementation and can call specific api endpoints of an exchange
        '''
        pass
