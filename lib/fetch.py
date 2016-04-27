import urllib.request


class Finam(object):
    """Fetch quotes from finam.ru"""
    ticker = None
    codes = {
        'MMM': '18090', 'T': '19067', 'ADBE': '20563', 'AA': '19997', 'GOOG': '20590', 'AXP': '18009', 'AIG': '19070',
        'AMT': '20568', 'AAPL': '20569', 'AMAT': '20570', 'BAC': '18011', 'BA': '18070', 'BRCM': '20575', 'CA': '20576',
        'CAT': '18026', 'CVX': '18037', 'CSCO': '20580', 'C': '18023', 'KO': '18076', 'GLW': '20582', 'DD': '18037',
        'EMC': '20585', 'EK': '22142', 'XOM': '18149', 'FSLR': '20586', 'GE': '18055', 'HPQ': '18068', 'HD': '18063',
        'IBM': '18069', 'IP': '22141', 'INTC': '19069', 'JPM': '18074', 'JNJ': '18073', 'MO': '18091', 'MCD': '18080',
        'MRK': '18094', 'MSFT': '19068', 'PFE': '18106', 'PG': '18107', 'TRV': '22139', 'UTX': '18134', 'VZ': '18137',
        'WMT': '18146', 'DIS': '18041', 'WFC': '22138', 'YHOO': '19075'
    }

    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_data(self, date_from, date_to, filename):
        if self.ticker not in self.codes:
            return
        fname = 'US2.' + self.ticker + '_' + date_from[2:4] + date_from[5:7] + date_from[8:10] + '_'
        fname += date_to[2:4] + date_to[5:7] + date_to[8:10]
        url = 'http://195.128.78.52/' + fname + '.csv?market=25&em=' + self.codes[self.ticker] + '&'
        url += 'code=US2.' + self.ticker + '&apply=0&'
        url += 'df=' + str(int(date_from[8:10])) + '&mf=' + str(int(date_from[5:7]) - 1) + '&yf=' + date_from[:4] + '&'
        url += 'from=' + date_from[8:10] + '.' + date_from[5:7] + '.' + date_from[:4] + '&'
        url += 'dt=' + str(int(date_to[8:10])) + '&mt=' + str(int(date_to[5:7]) - 1) + '&yt=' + date_to[:4] + '&'
        url += 'to=' + date_to[8:10] + '.' + date_to[5:7] + '.' + date_to[:4] + '&'
        url += 'p=2&f=' + fname + '&e=.csv&cn=US2.' + self.ticker + '&dtf=1&tmf=1&MSOR=0&mstimever=0&sep=3&sep2=1&datf=5'
        urllib.request.urlretrieve(url, filename)

    def fetch_year(self, year, notifications=False):
        if notifications:
            print('Starting: {}-{}'.format(self.ticker, year))
        self.fetch_data('{}-01-01'.format(year), '{}-12-31'.format(year),
                        '/srv/ft/data/' + self.ticker + '-{}.csv'.format(year))
