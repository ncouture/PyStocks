#!/usr/bin/env python
#

import urllib2
import csv
import re

__revision__ = "$Id: YahooFinance.py 7 2005-12-31 00:09:06Z nicolascouture $"

class FeedError(Exception):
    """
    Feed unavailable error.

    raised when obtaining data from a feed fails.
    """
    
    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__

class SymbolError(Exception):
    """
    Symbol invalid error.
    

    raised when a symbol is not valid.
    """
    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    ___str__ = __repr__

def format_number(n):
    """
    Convert a number to a string by adding a coma every 3 characters
    """
    n = str(n)
    return ','.join([n[::-1][x:x+3]
              for x in range(0,len(n),3)])[::-1]

class YahooQuoteFinder:
    """
    Find stocks quotes from Yahoo! Finances.
    """
    
    def __init__(self, symbol):
        """
        Download stock's attributes and attribute them to this object.
        
        * Basic attributes:

            symbol:       Our symbol
            company:      Our company name
            last_price:   Our price per share

            last_trade: (dict)
                date:     Last trade date
                time:     Last trade time
        
            change: (dict)
                cash:     Change in cash
                percent:  Change in percentage
                total:    Total volume of shares
                daily:    Average daily volume

            value: (dict)
                total:    Company's value (last price * volume)
                bid:      Bid
                ask:      Ask
                p_close:  Previous close price per share
                l_close:  Last close price per share

            range: (dict)
                day:      Day's Hi and Low
                year:     52-Week Hi and Low

            EPS:          Earning Per Share
            PE:           Price-Earnings Ratio

            dividend: (dict)
                l_date:   Dividend pay date
                p_share:  Dividend per share
                yeild:    Dividend yeild
        
            capital:      Market cap (volume * price)
            exchange:     Exchange name

        * Extended attributes:

            short_ratio:  Short Interest Ratio
            target_52w:   Targetted price in 52 weeks

            EPS_est: (dict)
                current_year: Estimated EPS this year
                next_year:    Estimated EPS next year
                next_quarter: Estimated EPS next quarter

            price_EPS_est: (dict)
                current_year: Estimated Price/EPS this year
                next_year:    Estimated Price/EPS next year
                next_quarter: Estimated Price/EPS next quarter

            PEG:          Price/Earnings to Growth
            book_value:   Book value
            price_book:   Price/Book
            EBITDA:       EBITDA

            average_move: (dict)
                d50:      50 days moving average
                d200:     200 days moving average

        * Real-Time attributes:

            realtime: (dict)
                ask:      Ask (real-time)
                bid:      Bid (real-time)

                change: (dict)
                    percent: Change percentage (real-time)
                    cash:    Change in money (real-time)

                last_trade: (dict)
                    date:    Last trade date (real-time)
                    price:   Last trade price (real-time)
                day_range:   Day range (real-time)
                capital:     Market cap (volume * price) (real-time)

        example:

            >>> YHOO = YahooQuoteFinder('YHOO')
            >>> YHOO.symbol
            'YHOO'
            >>> YHOO.realtime['last_trade']['date']
            'Dec 23'
            >>>
        """
        self.symbol = symbol
        
        # url: 43 attributes in a csv file
        self.url = "http://quote.yahoo.com/d?f=snl1d1t1c1p2va2bapomwerr1dyj"
        self.url += "1xs7t8e7e8e9r6r7r5b4p6p5j4m3m4b2b3k2k1c6m2j3&s=%s" % symbol

        # obtain stocks attributes
        try:
            f = urllib2.urlopen(self.url)
        except urllib2.URLError, e:
            raise FeedError("Could not fetch stocks attributes")


        # read the csv file, create the list of our attributes
        # and remove unwanted sgml tags
        reader = csv.reader(f)
        for l in reader: self.data = l
        for (pos, item) in enumerate(self.data):
            self.data[pos] = re.sub ('<[^>]*>', '', self.data[pos])

        # If the volume of shares is not available,
        # it is an invalid symbol
        if self.data[7] == 'N/A':
            raise SymbolError("Invalid symbol: %s" % symbol)

        
        """
        Basic Attributes
        """

        (self.symbol, self.company, self.last_price) = self.data[:3]

        # date, time
        self.last_trade = {'date': self.data[3],
                           'time': self.data[4]}

        # money change, percent change
        self.change = {'cash': self.data[5],
                       'percent': self.data[6]}

        # total volume, average daily volume
        self.volume = {'total': self.data[7],
                       'daily': self.data[8]}

        # company value, share bid, share ask,
        #  previous close, last close
        self.value = {'total': float(self.last_price
                                     ) * float(self.volume['total']),
                      'bid': self.data[9],
                      'ask': self.data[10],
                      'p_close': self.data[11],
                      'l_close': self.data[12]}

        # day range, 52weeks range
        self.range = {'day': self.data[13],
                      'year': self.data[14]}

        (self.EPS, self.PE) = (self.data[15], self.data[16])

        # div pay date, div per share, div yeild
        self.dividend = {'pay_date': self.data[17],
                         'per_share': self.data[18],
                         'yeild': self.data[19]}

        (self.capital, self.exchange) = (self.data[20], self.data[21])

        
        """
        Extended Attributes
        """

        (self.short_ratio,
         self.target_52w) = self.data[22:24]
        
        # estimate EPS - current year, next year, next quarter
        self.EPS_est = {'current_year': self.data[24],
                        'next_year': self.data[25],
                        'next_quarter': self.data[26]}
        
        # estimate price and EPS
        self.price_EPS_est = {'current_year': self.data[27],
                              'next_year': self.data[28],
                              'next_quarter': self.data[29]}

        (self.PEG,
         self.book_value,
         self.price_book,
         self.price_sales,
         self.EBITDA) = self.data[29:34]

        self.average_move = {'d50': self.data[34],
                             'd200': self.data[35]}


        """
        Real-Time Attributes
        """

        self.realtime = {'ask': self.data[36],
                         'bid': self.data[37],
                         'change': {'percent': self.data[38],
                                    'cash': self.data[40]},
                         'last_trade': {'date': self.data[39].split(" - ")[0],
                                        'price': self.data[39].split(" - ")[1]},
                         'day_range': self.data[41],
                         'capital': self.data[42]}



