from speculator.features.TechnicalAnalysis import TechnicalAnalysis
from speculator.utils import poloniex
from speculator.utils import stats

class RSI(TechnicalAnalysis):
    """
    Relative Strength Index:
    RSI = 100 - (100 / (1 + RS))
        such that,
            RS = avg(t-period gain) / avg(t-period loss)
    """

    def eval_algorithm(gains, losses):
        """ Evaluates the RSI algorithm

        Args:
            gains: List of price gains.
            losses: List of prices losses.

        Returns:
            Float between 0 and 100, momentum indicator
            of a market measuring the speed and change of price movements.
        """
        return 100 - (100 / (1 + RSI.eval_rs(gains, losses)))

    def eval_rs(gains, losses):
        """ Evaluates the RS variable in RSI algorithm

        Args:
            gains: List of price gains.
            losses: List of prices losses.

        Returns:
            Float of average gains over average losses.
        """
        # Number of days that the data was collected through
        count = len(gains) + len(losses)

        avg_gains = stats.avg(gains, count=count) if gains else 1
        avg_losses = stats.avg(losses,count=count) if losses else 1
        if avg_losses == 0:
            return avg_gains
        else:
            return avg_gains / avg_losses

    def eval_from_json(json):
        """ Gets RSI from a JSON of market data

        Args:
            json: List of dates where each entry is a dict of raw market data.

        Returns:
            Float between 0 and 100, momentum indicator
            of a market measuring the speed and change of price movements.
        """
        changes = poloniex.get_gains_losses(poloniex.parse_changes(json))
        return RSI.eval_algorithm(changes['gains'], changes['losses'])
