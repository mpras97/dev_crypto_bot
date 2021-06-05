from datetime import datetime
from math import floor

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager

from api import utils
from exchanges.exchange import Exchange
from models.order import Order
from models.price import Price


class Binance(Exchange):
    """
    Refers to the binance exchange
    """
    def __init__(self, key: str, secret: str):
        """
        Override parent init to setup the binance client
        """
        super().__init__(key, secret)

        self.client = Client(self.apiKey, self.apiSecret)
        self.name = self.__class__.__name__

    def get_client(self):
        """
        Return current client
        """
        return self.client

    def get_symbol(self):
        """
        Return the symbol representation of the given currency and asset
        """
        return self.currency + self.asset

    def symbol_ticker(self):
        """
        Return the price of the symbol? Confirm
        """
        response = self.client.get_symbol_ticker(symbol=self.get_symbol())
        return Price(
            pair=self.get_pair(),
            currency=self.currency.lower(),
            asset=self.asset.lower(),
            exchange=self.name.lower(),
            current=response["price"])

    def symbol_ticker_candle(self, interval=Client.KLINE_INTERVAL_1MINUTE):
        return self.client.get_klines(symbol=self.get_symbol(), interval=interval)

    def historical_symbol_ticker_candle(self, start: datetime, end=None, interval=Client.KLINE_INTERVAL_1MINUTE):
        """
        """
        # Convert default interval to string
        if isinstance(interval, int):
            interval = str(floor(interval / 60)) + "m"

        output = []
        for candle in self.client.get_historical_klines_generator(self.get_symbol(), interval, start, end):
            output.append(
                Price(pair=self.compute_symbol_pair(),
                    currency=self.currency.lower(),
                    asset=self.asset.lower(),
                    exchange=self.name.lower(),
                    current=candle[1],
                    lowest=candle[3],
                    highest=candle[2],
                    volume=candle[5],
                    openAt=utils.format_date(datetime.fromtimestamp(int(candle[0])/100)))
                )

        return output

    def get_asset_balance(self, currency):
        """
        Get asset balance for a given currency
        """
        response = self.client.get_asset_balance(currency)
        return response["free"]

    def order(self, order: Order):
        """
        Place an order with the binance client
        """
        return self.client.create_order(
            symbol=order.symbol,
            side=order.side,
            type=order.type,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=order.quantity,
            price=order.price
            )

    def test_order(self, order: Order):
        """
        Test whether the order is working with a custom order
        """
        return self.client.create_test_order(
            symbol=order.symbol,
            side=order.side,
            type=order.type,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=order.quantity,
            price=order.price
        )

    def check_order(self, orderId):
        """
        Check the order status
        """
        return self.client.get_order(
            symbol=self.get_symbol(),
            orderId=orderId
            )

    def cancel_order(self, orderId):
        """
        Cancel the order at the orderId
        """
        return self.client.cancel_order(
            symbol=self.get_symbol(),
            orderId=orderId
            )

    def get_socket_manager(self):
        """
        """
        return BinanceSocketManager(self.client)

    def start_symbol_ticker_socket(self, symbol: str):
        self.socketmanager = self.get_socket_manager()
        self.socket = self.socketmanager.start_symbol_ticker_socket(
            symbol=self.get_symbol(),
            callback=self.websocket_event_handler
            )
        self.start_socket()

    def websocket_event_handler(self, msg):
        if msg["e"] == "error":
            logging.warning(msg)
            self.close_socket()
        else:
            self.strategy.set_price(
                Price(pair=self.compute_symbol_pair(),
                    currency=self.currency,
                    asset=self.asset,
                    exchange=self.name,
                    current=msg["b"],
                    lowest=msg["l"],
                    highest=msg["h"])
                )
            self.strategy.run()
