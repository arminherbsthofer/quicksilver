import matplotlib.pyplot as plt


class TradingVisualizer:
    def __init__(self, trading_interface):
        self.trading_interface = trading_interface

    def visualize(self, symbol):
        plt.figure(figsize=(16, 6))
        plt.title('Relative Performance')
        pv, = plt.plot(
            self.trading_interface.portfolio_value_history / self.trading_interface.portfolio_value_history[0])
        av, = plt.plot(
            self.trading_interface.history[symbol]['Close'] / self.trading_interface.history[symbol]['Close'][0])
        plt.legend([pv, av], ['Rel. Portfolio Development', 'Rel. Asset Development'])
        plt.show()

        plt.figure(figsize=(16, 6))
        plt.title('Cash & Position Value')
        ch, = plt.plot(self.trading_interface.cash_history)
        ph, = plt.plot(self.trading_interface.position_value_history)
        plt.legend([ch, ph], ['Cash', 'Positions'])
        plt.show()
