"""
Stochastic Oscillator:
%K = 100 * (C - L(t)) / (H14 - L(t))
    such that,
        C = Current closing Price
        L(t) = Lowest Low over some duration t
        H(t) = Highest High over some duration t
          * t is usually 14 days

%K follows the speed/momentum of a price in a market
"""
def stochastic_oscillator(closing, low, high):
    return 100 * (closing - low) / (high - low)

