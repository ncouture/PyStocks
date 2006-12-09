#!/usr/bin/python
# Author: Nicolas Couture - pystocks@stormvault.net
#

import os
import time
import cPickle

from pystocks.YahooFinance import YahooQuoteFinder

__version__ = "$Id:$"

class PortfolioError(Exception):
    """
    Raised when an action fails to be applied to a portfolio.
    """
    pass

class QuoteFinder(YahooQuoteFinder):
    """
    Gives the current price of a stock to PortfolioManager.
    """
    def __init__(self):
        pass
    
    def getCurrentPrice(self, symbol):
        """
        This is called by a PortfolioManager instance and
        returns a float.
        """
        YahooQuoteFinder.__init__(self, symbol)
        return float(self.last_price)

class StockContainer:
    """
    Represent a batch of shares.
    """
    def __init__(self,
                 service,
                 symbol,
                 amount,
                 price=None,
                 epoch=None):
        """
        service: callable used to obtain price per share with
                 the getCurrentPrice methode
        symbol : specify security
        amount : amount of shares
        price  : price paid  (default: current price)
        epoch  : time bought (default: current time)
        """
        self.service = service
        self.symbol = symbol
        self.amount = int(amount)
        self.price = price or service().getCurrentPrice(symbol)
        if epoch:
            self.time = int(epoch)
        else:
            self.time = int(time.time())

        if not hasattr(QuoteFinder, 'getCurrentPrice'):
            raise PortfolioError("callable must provide a"
                                 " `getCurrentPrice' methode")

    def getInitialValue(self):
        """
        Price paid. (float)
        """
        price = self.price
        return float(price * self.amount)
    
    def getCurrentValue(self):
        """
        Current sell value. (float)
        """
        price = self.service().getCurrentPrice(self.symbol)
        return float(price * self.amount)

    def getTotalGains(self):
        """
        Total gains. (float)
        """
        current = self.getCurrentValue()
        initial = self.getInitialValue()
        change = current - initial
        return change

    def owned_time(self):
        """
        Amount of days owned (int)
        """
        raise NotImplementedError #TODO

class PortfolioManager:
    """
    Manage a dictionary of stocks.

    portfolio[symbol] = (amount, price paid, when added)
    """
    def __init__(self,
                 name,
                 container=os.path.expanduser("~/.pystocks/"),
                 service=QuoteFinder):
        """
        Create or load an existing portfolio.

        name: specify portfolio
        container: portfolio container (default: ~/.pystocks)
        service: (callable)
                 Used to obtain current prices with
                 getCurrentPrice method (default: QuoteFinder)
        """
        self.name = name.lower()
        self.container = os.path.expanduser(container)
        self.portfolio = os.path.join(self.container,
                                      name + ".portfolio")
        self.service = service
        if not hasattr(QuoteFinder, 'getCurrentPrice'):
            raise PortfolioError("service callable must provide a"
                                 " `getCurrentPrice' methode")
        if not os.path.isdir(self.container):
            os.mkdir(self.container)

        if os.path.isfile(self.portfolio):
            self._reload()
        else:
            self.stocks = {}

    def __iter__(self):
        for key in self.stocks:
            yield key

    def __getitem__(self, key):
        return self.stocks[key.upper()]

    def __contains__(self, key):
        return key.upper() in self.stocks

    def __setitem__(self, key, val):
        """
        Manipulate portfolio data.

        symbol: set 'data' on this security
        data: must be a 3 tuple in format:

                (amount, price, time)

              amount: amount of shares owned
              price : price paid per share
              time  : bought time in Epoch format (i.e. time.time())
        """
        if type(data) is not tuple:
            raise PortfolioError("Can only store a 3 tuple")
        if len(data) != 3:
            raise PortfolioError("You must provide a 3 tuple")
        
        symbol = symbol.upper()
        (amount, price, epoch) = data
        if symbol in self.stocks:
            self.remove(symbol)
        self.add(symbol, amount, price, epoch)
        
    def __delitem__(self, symbol):
        symbol = symbol.upper()
        del(self.stocks[symbol])
        self._save()
        
    def __repr__(self):
        return `self.stocks`

    def add(self, symbol, amount, price=None, epoch=None):
        """
        Add a stock to portfolio.

        symbol: specify security
        amount: total shares to be added
        price : optional value of one share
                (default: current price)
        time  : optional bought time in Epoch format
                (default: current time)

        returns a 3 tuple (symbol, share amount, price)
        """
        symbol = symbol.upper()
        amount = int(amount)
        if amount < 0:
            raise PortfolioError("share amount must be positive")
        price = price or self._get_last_price(symbol)
        epoch = epoch or int(time.time())
            
        if not symbol in self.stocks:
            self.stocks[symbol] = []
        self.stocks[symbol].append(StockContainer(self.service,
                                                  symbol,
                                                  amount,
                                                  price,
                                                  epoch))
        self._save()
        return (symbol, amount, price)

    def remove(self, symbol, amount=0, price=None):
        """
        Remove a stock from portfolio.

        symbol: specify security
        amount: amount to remove (default: 0, remove all shares)
        price : if specified, only remove shares bought at 'price'

          * The amount and price values are mutually exclusive.

        Returns the amount of shares removed from portfolio.
        """
        if amount and price:
            raise PortfolioError("The 'amount' and 'price' values are"
                                 " mutually exclusive")

        symbol = symbol.upper()
        if not symbol in self.stocks:
            raise PortfolioError("Could not find '%s' in your portfolio" % symbol)

        removed = 0
        to_remove = int(amount)

        if amount == 0 and not price:
            for container in self.stocks[symbol]:
                removed += container.amount
            del(self.stocks[symbol])

        # remove all shares at 'price'
        if price:
            for (pos, shares) in enumerate(self.stocks[symbol]):
                print "Price: %s In Price: %s" % (price, shares.price)
                if shares.price == price:
                    removed += shares.amount
                    del(self.stocks[symbol][pos])
                    continue
            # if all share containers were removed, remove the reference
            if len(self.stocks[symbol]) == 0:
                del(self.stocks[symbol])

        # remove only 'amount' of shares
        elif to_remove != 0:
            while removed != to_remove:
                if len(self.stocks[symbol]) == 0:
                    break # no shares left to be removed
                
                for (pos, shares) in enumerate(self.stocks[symbol]):
                    if removed == to_remove:
                        break # we removed enough shares

                    # container that has less than what we
                    # need to remove
                    if shares.amount < to_remove:
                        # remove it entirely
                        removed += shares.amount
                        del(self.stocks[symbol][pos])

                    # container that has more than what we
                    # need to remove
                    elif shares.amount > to_remove:
                        # remove it partially
                        amount = (to_remove - removed)
                        shares.amount -= amount
                        removed += amount
                        if shares.amount == 0:
                            del(self.stocks[symbol][pos])

                    # container that has the exact amount
                    # we need to remove
                    elif shares.amount == to_remove:
                        # remove it entirely
                        amount = (to_remove - removed)
                        shares.amount -= amount
                        removed += amount
                        if shares.amount == 0:
                            del(self.stocks[symbol][pos])

        #
        ############################################################

        self._save()
        return removed

    def getProfitsFrom(self, symbol):
        """
        Obtain a sum of the profits made with 'symbol'.
        """
        symbol = symbol.upper()

        if not symbol in self.stocks:
            raise PortfolioError("You do not own shares of '%s'")

        total = 0
        last_price = self._get_last_price(symbol)
        current_price = last_price
        for shares in self.stocks[symbol]:
            paid_price = shares.getInitialValue()
            sell_price = shares.getCurrentValue()
            total += (sell_price - paid_price)
        return total

    def getTotalProfits(self):
        """
        Return a float that is the sum of profits for
        every security in portfolio.
        """
        total = 0
        for symbol in self.stocks:
            total += self.getProfitsFrom(symbol)
        return total

    def _get_last_price(self, symbol):
        service = self.service()
        return float(service.getCurrentPrice(symbol))

    def _save(self):
        f = open(self.portfolio, "w")
        cPickle.dump(self.stocks, f)
        f.close()
        self._reload()

    def _reload(self):
        f = open(self.portfolio, "r")
        self.stocks = cPickle.load(f)
        f.close()
