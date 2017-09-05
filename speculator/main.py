from speculator.features.implementations import rsi as rsi_imp

def main():
    print(rsi_imp.get_rsi_poloniex(unit='hour', count=4, currency_pair='USDT_NEO', period=900))

if __name__=='__main__':
    raise SystemExit(main())
