#!/usr/bin/env python
#

import urllib2

__revision__ = "$Id:$"

class YahooQuoteFinder:
    # Pimped Finance::YahooQuote which was proven reliable for 3 years
    # without modifications. See http://dirk.eddelbuettel.com/code/.
    """
    Find stocks quotes from Yahoo! Finances.

    """
    def __init__(self, extended=False, realtime=False):
        """
        If no arguments are specified when initializing the
        quote finder the following values will be returned as a list:
        
        0 Symbol
        1 Company Name
        2 Last Price
        3 Last Trade Date
        4 Last Trade Time
        5 Change
        6 Percent Change
        7 Volume
        8 Average Daily Vol
        9 Bid
        10 Ask
        11 Previous Close
        12 Today's Open
        13 Day's Range
        14 52-Week Range
        15 Earnings per Share
        16 P/E Ratio
        17 Dividend Pay Date
        18 Dividend per Share
        19 Dividend Yield
        20 Market Capitalization
        21 Stock Exchange
        
        If the extended argument is True, the following fields
        will be retrieved:
        
        0 Short ratio
        1 1yr Target Price
        2 EPS Est. Current Yr
        3 EPS Est. Next Year
        4 EPS Est. Next Quarter
        5 Price/EPS Est. Current Yr
        6 Price/EPS Est. Next Yr
        7 PEG Ratio
        8 Book Value
        9 Price/Book
        10 Price/Sales
        11 EBITDA
        12 50-day Moving Avg
        13 200-day Moving Avg

        If the realtime argument is True, the following fields
        will be retrieved:
        
        1 Ask (real-time)
        2 Bid (real-time)
        3 Change in Percent (real-time)
        4 Last trade with time (real-time)
        5 Change (real-time)
        6 Day range (real-time)
        7 Market-cap (real-time)
        """
        self.url             = "http://quote.yahoo.com/d?f=FORMAT&s="
        self.format_default  = "snl1d1t1c1p2va2bapomwerr1dyj1x"
        self.format_extended = "s7t8e7e8e9r6r7r5b4p6p5j4m3m4"
        self.format_realtime = "b2b3k2k1c6m2j3"

        if extended and realtime:
            raise ValueError("extended and realtime are mutually exclusive")
        elif extended:
            self.url = self.url.replace('FORMAT', self.format_extended)
        elif realtime:
            self.url = self.url.replace('FORMAT', self.format_realtime)
        else:
            self.url = self.url.replace('FORMAT', self.format_default)

    def get_quote(self, symbol):
        """
        Obtain a stock information by symbol.

        symbol: stock symbol
        """
        # postfix our url with the symbol
        url = self.url + symbol.upper()
        # obtain csv file
        f = urllib2.urlopen(url)
        # read the data into quote
        quote = f.read()
        # split, strip and replace parts of data obtained
        results = [f.strip().replace('"', '') for f in quote.split(",")]
        # return parsed results
        return results

symbol='YHOO'
# Default Stock Quotes
StockInfo = YahooQuoteFinder()
print "=== Default ==="
for i in StockInfo.get_quote(symbol):
    print i
print

# Extended Stock Quotes
ExtStockInfo = YahooQuoteFinder(extended=True)
print "=== MSFT Extended ==="
for i in ExtStockInfo.get_quote(symbol):
    print i
print

# Real Time Stocks Quotes
LiveStockInfo = YahooQuoteFinder(realtime=True)
print "=== Real Time ==="
for i in StockInfo.get_quote(symbol):
    print i
print

