import lib.indicators as indicators
import indicator.ema as ema

if __name__ == '__main__':
    # updater = indicators.MySQLIndicatorsUpdate('AAPL', 'ma', 'ema12')
    # ema = ema.EMA('AAPL', 12)
    updater = indicators.MySQLIndicatorsUpdate('AAPL', 'ma', 'ema12')
    ema = ema.EMA('AAPL', 12)
    for dtime, value in ema.get_all():
        updater.insert(dtime, value)
    updater.commit()
