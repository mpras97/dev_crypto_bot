
import logging
from datetime import datetime
from api import utils
from abc import ABC, abstractmethod
from twisted.internet import reactor
from strategies.strategy import Strategy
from models.order import Order


class Exchange(ABC):
    currency: str
    asset: str
    strategy: Strategy

    def __init__(self, key:str, secret:str):
        self.apiKey = key
        self.apiSecret = secret
        self.name = None
        self.client = None
        self.socketmanager = None
        self.socket = None
        self.currency = ""
        self.asset = ""
        self.strategy = None

    def set_currency(self, symbol: str):
        """
        Set currency symbol for the exchange
        # DO WE NEED THIS? WE CAN DIRECTLY USE setattr?
        """
        self.currency = symbol

    def set_asset(self, symbol: str):
        """
        Set asset symbol for the exchange
        # DO WE NEED THIS? WE CAN DIRECTLY USE setattr?
        """
        self.asset = symbol

    def set_strategy(self, strategy: Strategy):
        """
        Set strategy for the exchange
        # DO WE NEED THIS? WE CAN DIRECTLY USE setattr?
        """
        self.strategy = strategy

    def compute_symbol_pair(self):
        """
        Override the default implementation of formatting currency asset
        symbol formatting by binance
        """
        return utils.format_pair(self.currency, self.asset)

    """
    Abstract methods
    """

    @abstractmethod
    def get_symbol(self):
        """
        Override to show exchange symbol pair notation
        """
        return self.compute_symbol_pair(self)

    @abstractmethod
    def symbol_ticker(self):
        """
        Get symbol currency ticker
        """
        pass

    @abstractmethod
    def symbol_ticker_candle(self, interval):
        """
        Get current symbol ticker candle for the given interval
        """
        pass

    @abstractmethod
    def historical_symbol_ticker_candle(self, start: datetime, end=None, interval=60):
        """
        Get current symbol historical value
        """
        pass

    @abstractmethod
    def get_asset_balance(self, currency):
        """
        Get balance for the given currency
        """
        pass

    @abstractmethod
    def order(self, order: Order):
        """
        Order for the price in the exchange
        """
        pass

    @abstractmethod
    def check_order(self, orderId):
        """
        Check order status
        """
        pass

    @abstractmethod
    def cancel_order(self, orderId):
        """
        Cancel order at orderId
        """
        pass

    """
    Methods wrt web socket usage in the exchange
    """

    @abstractmethod
    def get_socket_manager(self):
        pass

    @abstractmethod
    def websocket_event_handler(self, msg):
        pass

    def start_socket(self):
        logging.info("Starting websocket connection...")
        self.socketmanager.start()

    def close_socket(self):
        self.socketmanager.stop_socket(self.socket)
        self.socketmanager.close()
        reactor.stop()

    @abstractmethod
    def start_symbol_ticker_socket(self, symbol: str):
        pass
