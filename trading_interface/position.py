class Position:
    def __init__(self, symbol, quantity, price, timestamp, action,
                 status='open', stop_loss=None, take_profit=None):
        '''
            symbol: ticker symbol of asset
            quantity: ordered quantity of symbol
            price:
            timestamp:
            action: 'long' or 'short'
            status: 'open' or 'closed'
            stop_loss: loss at which position must be closed
            take_profit: gain at which position must be closed
        '''
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.action = action
        self.status = status
        self.stop_loss = stop_loss
        self.take_profit = take_profit
