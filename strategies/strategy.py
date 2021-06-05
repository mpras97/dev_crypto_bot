import json
import threading
import time
from datetime import datetime
from decouple import config
from models.price import Price


class Strategy:
    """
    Abstract strategy used after creating all the strategies
    """
    price: Price

    def __init__(self, exchange, interval=60, *args, **kwargs):
        """
        """
        self._timer = None
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.portfolio = {}
        self.exchange = exchange
        # We load the account portfolio on load
        self.get_portfolio()

    def _run(self):
        """
        Internal method that starts running the strategy
        """
        self.is_running = False
        self.start()
        self.run(*self.args, **self.kwargs)

    def start(self):
        """
        The given method starts the API execution if the strategy is not running
        """
        if not self.is_running:
            print(datetime.now())
            if self._timer is None:
                self.next_call = time.time()
            else:
                self.next_call += self.interval

            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """
        Stops the timer thread which is running the strategy and sets
        is_running to False
        """
        self._timer.cancel()
        self.is_running = False

    def get_portfolio(self):
        """
        Gets the current portfolio of the user
        # TEST MOST PROBABLY THIS IS RETURNING A SINGLE STRATEGY
        """
        self.portfolio = {
            "currency": self.exchange.get_asset_balance(self.exchange.currency),
            "asset": self.exchange.get_asset_balance(self.exchange.asset)
            }

    def get_price(self):
        """
        Returns the exchange price
        """
        try:
            self.price = self.exchange.symbol_ticker()
        except Exception as e:
            pass
