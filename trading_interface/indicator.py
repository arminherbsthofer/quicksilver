import numpy as np


class Indicator:
    def __init__(self):
        pass

    def RSI(self, tohlcv, window, limit=1000, min_entries=10):
        epsilon = 0.000001

        close_price = np.array(tohlcv['Close'][-limit:])
        open_price = np.array(tohlcv['Open'][-limit:])

        change = close_price - open_price

        # if not enough data is given, return 50 because it is the neutral value for rsi
        if len(change) < window + min_entries:
            return np.repeat(50, window)

        gain = np.copy(change)
        gain[gain < 0] = 0

        loss = np.copy(change)
        loss[loss > 0] = 0
        loss = np.abs(loss)

        avg_gain = np.convolve(gain, np.ones(window) / window, mode='valid')
        avg_loss = np.convolve(loss, np.ones(window) / window, mode='valid')

        rs = avg_gain / (avg_loss + epsilon)

        return 100 - 100 / (1 + rs)
