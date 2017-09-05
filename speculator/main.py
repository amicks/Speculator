from speculator.features.implementations import rsi as rsi_imp
from speculator.features.implementations import stoch_osc as so_imp

def main():
    print('Relative Strength Index:')
    print(rsi_imp.rsi_poloniex(unit='hour', count=4, currency_pair='USDT_BTC', period=900))

    print('Stochastic Oscillator:')
    print(so_imp.so_poloniex(unit='hour', count=4, currency_pair='USDT_BTC', period=900))

if __name__=='__main__':
    raise SystemExit(main())
