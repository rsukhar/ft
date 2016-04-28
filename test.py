from lib.DB import DBInstaller
from lib.Fetch import Fetch

if __name__ == '__main__':
    DBInstaller().install(False)
    for year in range(2009, 2017):
        Fetch.import_quotes('AAPL', '/srv/ft/data/AAPL/quotes-' + str(year) + '.csv')
