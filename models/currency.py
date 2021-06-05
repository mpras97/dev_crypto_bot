from models.model import AbstractModel


class Currency(AbstractModel):
    """
    Stores the currency information
    """
    name: str = ''
    symbol: str = ''
    fiat: bool
