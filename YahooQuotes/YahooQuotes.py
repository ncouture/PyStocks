#!/usr/bin/env python
#

import urllib2

__revision__ = "$Id$"

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
        format = "snl1d1t1c1p2va2bapomwerr1dyj1xs7"
        format += "t8e7e8e9r6r7r5b4p6p5j4m3m4b2b3k2k1c6m2j3"
        url = "http://quote.yahoo.com/d?f=" + format
        url += "&s=" + symbol

        # download & read csv file
        try:
            f = urllib2.urlopen(url)
            quote = f.read()
        except urllib2.URLError, e:
            raise ValueError("An error occured when opening %s" % url)

        # split, strip and replace parts of data obtained
        self.data = []
        for f in quote.split(","):
            f = f.strip()
            f = f.replace('"', "")
            self.data.append(f)


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
                                                       
        

if __name__ == "__main__":
    # Default Stock Quotes
    import sys
    
    if len(sys.argv) != 2:
        print "Usage: YahooQuote.py <symbol>"
        sys.exit(1)
    
    Stock = YahooQuoteFinder(sys.argv[1])

    """
    Default
    """
    print
    print "Symbol: %s"             % Stock.symbol
    print "Company: %s"            % Stock.company
    print "Last Price: %s"         % Stock.last_price
    print "Last trade date: %s"    % Stock.last_trade['date']
    print "Last trade time: %s"    % Stock.last_trade['time']
    print "Day change: %s"         % Stock.change['cash']
    print "Day percent change: %s" % Stock.change['percent']
    print "Total volume: %s"       % Stock.volume['total']
    print "Daily volume: %s"       % Stock.volume['daily']
    print "Company value: %s"      % Stock.value['total']
    print "Bid: %s"                % Stock.value['bid']
    print "Ask: %s"                % Stock.value['ask']
    print "Previous close: %s"     % Stock.value['p_close']
    print "Last close: %s"         % Stock.value['l_close']
    print "Day range: %s"          % Stock.range['day']
    print "52W range: %s"          % Stock.range['year']
    print "Earning Per Share: %s"  % Stock.EPS
    print "Price / Earning: %s"    % Stock.PE
    print "Dividend pay date: %s"  % Stock.dividend['pay_date']
    print "Dividend per share: %s" % Stock.dividend['per_share']
    print "Dividend yeild: %s"     % Stock.dividend['yeild']
    print "Capitalization: %s"     % Stock.capital
    print "Exchange: %s"           % Stock.exchange
    

    """
    Extended
    """
    raw_input("\nPress any key to see Extended attributes ")
    print
    print "Short ratio: %s"           % Stock.short_ratio
    print "52w target: %s"            % Stock.target_52w
    print "EPS Est. 1 year: %s"       % Stock.EPS_est['current_year']
    print "EPS Est. next year: %s"    % Stock.EPS_est['next_year']
    print "EPS Est. next quarter: %s"      % Stock.EPS_est['next_quarter']
    print "Price/EPS Est. 1 year: %s" % Stock.price_EPS_est['current_year']
    print "Price/EPS Est. next year: %s"   % Stock.price_EPS_est['next_year']
    print "Price/EPS Est. next quater: %s" % (
        Stock.price_EPS_est['next_quarter'])
    print "Price/Earnings to Growth: %s"   % Stock.PEG
    print "Book value: %s"            % Stock.book_value
    print "Price/Book: %s"            % Stock.price_book
    print "EBITDA: %s"                % Stock.EBITDA
    print "50 days moving average: %s"     % Stock.average_move['d50']
    print "200 days moving average: %s"    % Stock.average_move['d200']

    """
    Real-Time (after-hours)
    """
    raw_input("\nPress any key to see Real-Time attributes ")
    print
    print "Ask (real-time): %s"            % Stock.realtime['ask']
    print "Bid (real-time): %s"            % Stock.realtime['bid']
    print "Change percent (real-time): %s" % Stock.realtime['change']['percent']

    print "Change in cash (real-time): %s" % (
        Stock.realtime['change']['cash'])

    print "Last trade date (real-time): %s" % (
        Stock.realtime['last_trade']['date'])
    
    print "Last trade price (real-time): %s" % (
        Stock.realtime['last_trade']['price'])

    print "Day range (real-time): %s" % Stock.realtime['day_range']
    print "Market Capitalization: %s" % Stock.realtime['capital']
    print
    
