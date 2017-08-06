from __future__ import absolute_import, division, print_function

import logging
from datetime import datetime
from datetime import timedelta
from threading import Lock
from functools import wraps
import uuid
import random

from sssm.backend import (
    Store, 
    CommonStock, 
    PreferredStock, 
    Trader, 
    Transaction, 
    Shares_Trading
)

from sssm.backend.util import validate_stock

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Platform():
    """ Trading platform for traders. It simulates ~30mins of trade
        using the Platform.simulate() method for testing.
        
    """
    
    def __init__(self, store=None, p_stock_orm=None, 
                    c_stock_orm=None, shares_trading_orm=None):
        
        if store:
            self._store = store
        else:
            self._store = Store()
       
        self._common_stock = c_stock_orm if c_stock_orm else CommonStock(store=self._store)
        self._preferred_stock = p_stock_orm if p_stock_orm else PreferredStock(store=self._store)
        self._shares_trading = shares_trading_orm if shares_trading_orm else Shares_Trading(store=self._store)

    def simulate(self):
        base_price = 22.0
        stocks = ['TEA', 'GIN', 'JOE', 'ALE', 'POP']
        trade_types = ['SELL', 'BUY']
      
        traders = []
        tokens = []

        # create traders
        for i in range(100):
            trader = uuid.uuid4()
            traders.append(str(trader))
            td = Trader(str(trader), store=self._store)
            tokens.append(td.save())

            # trading times: simulate 30mins of trading
        now = datetime.now()
        txn_times = [now - timedelta(seconds=i) for i in range(1800)]
        txn_ids = []

        for time in txn_times:
            idx = random.randint(0, 99)
            qty = random.randrange(1, 10000, 1)
            ttype_idx = random.randint(0, 1)
            stocks_idx = random.randint(0, 4)
            price = base_price + 10 * random.random()

            try:        
                txn_ids.append(self.trade(traders[idx], tokens[idx], stocks[stocks_idx], 
                    qty, price, trade_type=trade_types[ttype_idx], timestamp=time))

            except ValueError:
                pass    
        
    @validate_stock('Platform')
    def create_user(id):
        return Trade(id, store=self.store).save()
    
    def pe_ratio(self, symbol, price):
        pass
    
    #@validate_stock('Platform')
    def trade(self, trader, token, symbol, qty, 
              price, trade_type='BUY', timestamp=datetime.now()):
        """ Function to conduct trader with input parameters.
            
        Parameters
        ----------
        trader : str
            Id of trader
        token : str
            access token obtained by trader at registration
        symbol : str
            symbol of stock to trade
        qty : int
            quantity of stock to trade
        price : float
            stock price
        trade_type : str
            indicator for trade type: BUY or SELL
        timestamp : datetime.datetime
            time to record against trade
            
        Return
        ------
        txnid : str
            Id of saved/recorded transaction
            
        Example
        -------
        >>> from sssm.backend import Platform, Store
        >>> trader = 'trader1'
        >>> t = Trader(trader)
        >>> token = t.save()
        >>> stock = 'GIN'
        >>> qty = 1000
        >>> price = 15.0
        >>> s = Store()
        >>> p = Platform(s)
        >>> p.trade(trader, token, stock, qty, price, trade_type='SELL')
        UUID('1317e634-4b7a-459a-b0d5-55beb351c190')
        
        """
        if not symbol:
            raise ValueError("[ERROR] Platform: Stock symbol must be provided.")

        if not qty:
            raise ValueError("[ERROR] Platform: Stock quantity must be provided.")
                
        trd = Trader(trader, store=self._store)
        t = trd.load(trader) 
        
        #logging.debug('[INFO] Platform: Recording trade for trader .....{}'.format(t))
        
        if token is not t['token']:
            raise ValueError("[ERROR] Platform: Failed authentication. Token doesn't match record.")
           
        trader_has_stock = False
        
        # buy/sell from/to shares trading
        if trade_type == 'SELL':
            # verify that trader have stock and in enough qty
            portfolio = t['portfolio']
            for record in portfolio:
                if record['symbol'] == symbol:
                    trader_has_stock = True
                    
                    if record['qty'] < qty:
                        raise ValueError("[ERROR] Platform: Trader {} doesn't '\
                        'have sufficient qty for stock {}". format(trader, symbol))
                    
                    break
                    
            if not trader_has_stock:
                raise ValueError("[ERROR] Platform: Trader {} doesn't '\
                        'have stock {}". format(trader, symbol))
        else:
            if self._shares_trading.get_qty(symbol) < qty:
                raise ValueError("[ERROR] Platform: Stock {} doesn't '\
                        'exist in sufficient qty {}". format(symbol, qty))
            
            self._shares_trading.buy(symbol, qty) 
            
        # update portfolio
        portfolio = t['portfolio']
        
        updated = False
        
        if len(portfolio) > 0:
            for record in portfolio:
                if record['symbol'] == symbol:
                    if trade_type == 'BUY':
                        record['qty'] += qty
                    else:
                        record['qty'] -= qty
                    updated = True
                    
            if not updated:
                record = {
                    'symbol':symbol,
                    'qty': qty,
                    'price': price
                }
                
                portfolio.append(record)
        else:
            record = {
                    'symbol':symbol,
                    'qty': qty,
                    'price': price
                }
                
            portfolio.append(record)
                
        trd.portfolio = portfolio
        
        trd.save()
        
        # update stock price
        if self._store.get_type(symbol) == "Preferred":
            PreferredStock(self._store).set_current_price(symbol, price)
        else:
            CommonStock(self._store).set_current_price(symbol, price)
            
        # record trade that has just occured
        txn = Transaction(symbol, qty, price, 
                 timestamp=timestamp, user=t['id'],
                 store=self._store, trade_type=trade_type)
        
        txnid = txn.save()
        
        return txnid
    
    @validate_stock('Platform')
    def compute_dividend_yield(self, symbol, price):
        """
        Compute dividend yield given ``stock symbol`` and its ``price``.
        Determines the type of stock prior to computing dividend.

        Parameters
        ----------
        symbol : str
            Stock symbol to compute dividend yield for.
        price : float
            Price of stock (symbol)

        Examples
        --------
        >>> from sssm.backend import Platform
        >>> stock_symbol = 'TEA'
        >>> price = 25.0
        >>> platform.compute_dividend_yield(stock_symbol, price)
        0

        Returns
        -------
        yield : float
            Stock's dividend yield.

        """

        stock_type = self.store.get_type(symbol)

        if stock_type == "Preferred":
            return PreferredStock(self.store).dividend_yield(symbol, price)

        return CommonStock(self.store).dividend_yield(symbol)
        
    def volume_weighted_stock_price(self, since=15, time_ref=None):
        """
        Volume weighted stock price within given interval - default 15 mins.
        
        Parameters
        ----------- 
        since : int
            interval in mins since trade occured
            
        ref : datetime
            Reference of date/time from which relative time (``since``) should start.
            
        Returns
        -------
        price : float
            weighted volume stock price computed on given interval.
            
        """
        start_dt = time_ref if time_ref else datetime.now()
        
        qty = []
        price_qty = []
        
        txn_orm = Transaction(None, None, 'TEA', store=self._store)
        ids = txn_orm.find(start_dt - timedelta(minutes=since))
        
        for txn_id in ids:
            if txn_id:
                txn = txn_orm.load(txn_id)
                price_qty.append(txn['volume'] * txn['per_price'])
                qty.append(txn['volume'])
        
        if len(qty) == 0:
            raise ValueError("[ERROR] Platform: No transaction found.")
            
        return sum(price_qty) / sum(qty)
    
    def all_share_index(self):

        """ Obtain all share index for stock prices.
        """
        
        # let's leverage numpy capabilities
        import numpy as np
            
        shares_trading = self._store.get_shares_trading()
        
        shares_prices = [PreferredStock(self._store).get_current_price(symbol) \
                         if self._store.get_type(symbol) == 'Preferred' else \
                         CommonStock(self._store).get_current_price(symbol) for \
                         symbol in shares_trading \
                        ]
        shares_prices = np.array(shares_prices)
        
        return shares_prices.prod()**(1.0/len(shares_prices))