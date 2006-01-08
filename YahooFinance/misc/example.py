#!/usr/bin/env python


from YahooFinance import YahooQuoteFinder, FeedError, SymbolError

Stock = YahooQuoteFinder('YHOO')

import sys
    
if len(sys.argv) != 2:
    print "Usage: YahooQuote.py <symbol>"
    sys.exit(1)

try:
    Stock = YahooQuoteFinder(sys.argv[1])

#Unable to obtain data from feed
except FeedError, e: 
    print e
    sys.exit(1)

#Unable to lookup symbol
except SymbolError, e:
    print e
    sys.exit(1)


"""
Basic Atributes
"""

print
print "Symbol: %s"             % Stock.symbol
print "Company: %s"            % Stock.company
print "Last Price: %s"         % Stock.last_price
print "Last trade date: %s"    % Stock.last_trade['date']
print "Last trade time: %s"    % Stock.last_trade['time']
print "Day change: %s"         % Stock.change['cash']
print "Day percent change: %s" % Stock.change['percent']
print "Total volume: %s"       % Stock.volume['average']
print "Daily volume: %s"       % Stock.volume['daily']
print "Company value: %s"      % Stock.volume['average']
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
    
