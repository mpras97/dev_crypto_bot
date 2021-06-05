import logging
from exchanges.exchange import Exchange
from strategies.strategy import Strategy


class Watcher(Strategy):
    """
    The given strategy simply prints the current exchange prices
    """

    def run(self):
        """
        Run to get the price at regular intervals
        """
        self.get_price()
        logging.info("**********************************")
        logging.info("Exchange: ", self.exchange.name)
        logging.info("Pair: ", self.exchange.get_symbol())
        logging.info("Available: ", self.portfolio["currency"] + ' ' + self.exchange.currency)
        logging.info("Available: ", self.portfolio["asset"] + ' ' + self.exchange.asset)
        logging.info("Price: ", self.price.current)
