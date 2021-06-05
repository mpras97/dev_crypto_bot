import sys
from datetime import datetime

from exchanges.exchange import Exchange
from models.dataset import Dataset
from models.price import Price


class BackTest:

    def __init__(self, exchange: Exchange, period_start: datetime, period_end: None, interval=60):
        self.launchedAt = datetime.now()

        dataset = Dataset().query("get", {
            "exchange": "/api/exchanges/" + exchange.name.lower(),
            "currency": "/api/currencies/" + exchange.currency.lower(),
            "asset": "/api/currencies/" + exchange.asset.lower(),
            "period_start": period_start,
            "period_end": period_end,
            "candleSize": interval
            })

        if dataset and len(dataset) > 0:
            logging.info(dataset[0])
            price = Price()
            for price in price.query("get", {"dataset": dataset[0]["uuid"]}):
                newPrice = Price()
                newPrice.populate(price)
                exchange.strategy.set_price(newPrice)
                exchange.strategy.run()
        else:
            logging.info("Dataset not found, external API calls to: " + exchange.name)
            for price in exchange.historical_symbol_ticker_candle(period_start, period_end, interval):
                exchange.strategy.set_price(price)
                exchange.strategy.run()

        execution_time = datetime.now() - self.launchedAt
        logging.info("Execution time: " + str(execution_time.total_seconds()) + " seconds")
        sys.exit()
