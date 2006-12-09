#!/usr/bin/env python


from YahooFinance import YahooQuoteFinder
from YahooFinance import FeedError, SymbolError

stock = YahooQuoteFinder('YHOO')

import sys
    
if len(sys.argv) != 2:
    print "Usage: YahooQuote.py <symbol>"
    sys.exit(1)

try:
    stock = YahooQuoteFinder(sys.argv[1])

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
print "Symbol: %s"             % stock.symbol
print "Company: %s"            % stock.company
print "Last Price: %s"         % stock.last_price
print "Last trade date: %s"    % stock.last_trade['date']
print "Last trade time: %s"    % stock.last_trade['time']
print "Day change: %s"         % stock.change['cash']
print "Day percent change: %s" % stock.change['percent']
print "Total volume: %s"       % stock.volume['average']
print "Daily volume: %s"       % stock.volume['daily']
print "Company value: %s"      % stock.volume['average']
print "Bid: %s"                % stock.value['bid']
print "Ask: %s"                % stock.value['ask']
print "Previous close: %s"     % stock.value['p_close']
print "Last close: %s"         % stock.value['l_close']
print "Day range: %s"          % stock.range['day']
print "52W range: %s"          % stock.range['year']
print "Earning Per Share: %s"  % stock.EPS
print "Price / Earning: %s"    % stock.PE
print "Dividend pay date: %s"  % stock.dividend['pay_date']
print "Dividend per share: %s" % stock.dividend['per_share']
print "Dividend yeild: %s"     % stock.dividend['yeild']
print "Capitalization: %s"     % stock.capital
print "Exchange: %s"           % stock.exchange
    


"""
Extended
"""
raw_input("\nPress any key to see Extended attributes ")
print
print "Short ratio: %s"           % stock.short_ratio
print "52w target: %s"            % stock.target_52w
print "EPS Est. 1 year: %s"       % stock.EPS_est['current_year']
print "EPS Est. next year: %s"    % stock.EPS_est['next_year']
print "EPS Est. next quarter: %s"      % stock.EPS_est['next_quarter']
print "Price/EPS Est. 1 year: %s" % stock.price_EPS_est['current_year']
print "Price/EPS Est. next year: %s"   % stock.price_EPS_est['next_year']
print "Price/EPS Est. next quater: %s" % (
    stock.price_EPS_est['next_quarter'])
print "Price/Earnings to Growth: %s"   % stock.PEG
print "Book value: %s"            % stock.book_value
print "Price/Book: %s"            % stock.price_book
print "EBITDA: %s"                % stock.EBITDA
print "50 days moving average: %s"     % stock.average_move['d50']
print "200 days moving average: %s"    % stock.average_move['d200']


"""
Real-Time (after-hours)
"""

raw_input("\nPress any key to see Real-Time attributes ")
print
print "Ask (real-time): %s"            % stock.realtime['ask']
print "Bid (real-time): %s"            % stock.realtime['bid']
print "Change percent (real-time): %s" % stock.realtime['change']['percent']

print "Change in cash (real-time): %s" % (
    stock.realtime['change']['cash'])

print "Last trade date (real-time): %s" % (
    stock.realtime['last_trade']['date'])

print "Last trade price (real-time): %s" % (
    stock.realtime['last_trade']['price'])

print "Day range (real-time): %s" % stock.realtime['day_range']
print "Market Capitalization: %s" % stock.realtime['capital']
print
    
"""
Fundamental information
"""

print "Oustanding shares:", stock.outstanding
print "Floating shares:", stock.float
print "Restricted shares:", stock.restricted

