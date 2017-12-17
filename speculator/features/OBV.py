from speculator.features.TechnicalAnalysis import TechnicalAnalysis
from speculator.utils import poloniex

class OBV(TechnicalAnalysis):
    """
    On Balance Volume:
    OBV = OBV_prev + v
        such that,
            v = volume  if close >  close_prev
            v = 0       if close == close_prev
            v = -volume if close <  close_prev
    """

    def eval_algorithm(curr, prev):
        """ Evaluates OBV

        Args:
            curr: Dict of current volume and close
            prev: Dict of previous OBV and close

        Returns:
            Float of OBV
        """
        if curr['close'] > prev['close']:
            v = curr['volume']
        elif curr['close'] < prev['close']:
            v = curr['volume'] * -1
        else:
            v = 0
        return prev['obv'] + v

    def eval_from_json(json):
        """ Gets OBV from a JSON of market data

        Args:
            json: List of dates where each entry is a dict of raw market data.

        Returns:
            Float of OBV
        """
        closes = poloniex.get_attribute(json, 'close')
        volumes = poloniex.get_attribute(json, 'volume')
        obv = 0
        for date in range(1, len(json)):
            curr = {'close': closes[date], 'volume': volumes[date]}
            prev = {'close': closes[date - 1], 'obv': obv}
            obv = OBV.eval_algorithm(curr, prev)
        return obv
