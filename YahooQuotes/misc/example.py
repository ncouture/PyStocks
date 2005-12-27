#!/usr/bin/env python
#

from YahooQuotes import YahooQuoteFinder

Stock = YahooQuoteFinder('YHOO')

print
"""
Basic attributes
"""
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


raw_input("\nPress a key to see Extended attributes ")
print

"""
Extended attributes
"""
print "Short ratio: %s"           % Stock.short_ratio
print "52w target: %s"            % Stock.target_52w
print "EPS Est. 1 year: %s"       % Stock.EPS_est['current_year']
print "EPS Est. next year: %s"    % Stock.EPS_est['next_year']
print "EPS Est. next quarter: %s"      % Stock.EPS_est['next_quarter']
print "Price/EPS Est. 1 year: %s" % Stock.price_EPS_est['current_year']
print "Price/EPS Est. next year: %s"   % Stock.price_EPS_est['next_year']
print "Price/EPS Est. next quater: %s" % Stock.price_EPS_est['next_quarter']
print "Price/Earnings to Growth: %s"   % Stock.PEG
print "Book value: %s"            % Stock.book_value
print "Price/Book: %s"            % Stock.price_book
print "EBITDA: %s"                % Stock.EBITDA
print "50 days moving average: %s"     % Stock.average_move['d50']
print "200 days moving average: %s"    % Stock.average_move['d200']

raw_input("\nPress a key to see Real-Time attributes ")
print

"""
Real-Time attributes
"""
