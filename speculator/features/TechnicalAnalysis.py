import abc

class TechnicalAnalysis(abc.ABC):
    """ Abstract class for calculating technical analysis indicators """
    
    @staticmethod
    @abc.abstractmethod
    def eval_algorithm(*args, **kwargs):
        """ Evaluates TA algorithm """

    @staticmethod
    @abc.abstractmethod
    def eval_from_json(json):
        """ Evaluates TA algorithm from JSON

        Args:
            json: List of dates where each entry is a dict of raw market data.
        """
