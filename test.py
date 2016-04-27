from lib.Fetch import Fetch
from lib.DB import *

if __name__ == '__main__':
    Fetch.import_quotes('AAPL', '/srv/ft/data/AAPL-2010.csv')