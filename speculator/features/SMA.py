from speculator.features.TechnicalAnalysis import TechnicalAnalysis
from speculator.utils import poloniex
from speculator.utils import stats

class SMA(TechnicalAnalysis):
    """
    Simple Moving Average:
    Average closing price over a period
    SMA = avg(closes) = sum(closes) / len(closes)
    """

    def eval_algorithm(closes):
        """ Evaluates the SMA algorithm

        Args:
            closes: List of price closes.

        Returns:
            Float average of closes.
        """
        return stats.avg(closes)

    def from_poloniex(json):
        """ Gets SMA from a JSON of market data

        Args:
            json: List of dates where each entry is a dict of raw market data.

        Returns:
            Float average of closes.
        """
        closes = [date['close'] for date in json]
        return SMA.eval_algorithm(closes)
