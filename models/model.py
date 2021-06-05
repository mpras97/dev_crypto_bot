from datetime import datetime


class AbstractModel:
    """
    Base model used at multiple places for usage as abstract
    """
    created: datetime

    def __init__(self, **kwargs):
        """
        We set all keys of dictionary as an attribute of the class
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
