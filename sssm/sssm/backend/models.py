from __future__ import absolute_import, division, print_function

from datetime import datetime
from functools import wraps
from sssm.backend import Store
from sssm.backend.util import validate_stock
import uuid
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Trader(object):
    """ Record mapper and data access class for users.
    
    Examples
    --------
    
    >>> from sssm.backend import User
    >>> id = 'trader1'
    >>> u = Trader(id)
    
    """
    
    def __init__(self, trader_id, store=None, token=None, created=None):
    
        if not trader_id:
            raise ValueError("[ERROR] Models: Trader ID must be provided.")
            
        self._id = trader_id 
        self._token = token if token else uuid.uuid4() 
        self._store = store if store else Store()
        self._created = created if created else datetime.now()
    
    @property    
    def id():
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        
    @property    
    def token():
        return self._token
    
    @token.setter
    def token(self, token):
        self._token = token
    
    @property    
    def created():
        return self._created
    
    @created.setter
    def created(self, created):
        self._created = created
        
    def save(self):
        if self._id in self._store.get_traders():
            return ValueError()
        
        self._record = {
                'id': self._id,
                'token': self._token,
                '_type': 'User',
                'created' : self._created
            }
        
        self._store['traders'][self._id] = self._record
        
        return self._token
    
    def load(self, id):
        self._record = self._store['traders'][id]
        self._load(self._record)
        
        return self._record
    
    def _load(self, record):
        self._id = record['id']
        self._token = record['token']
        self._created = record['created']
    
class Transaction(object):
    """ A Trade - Record mapper and data access class for trades.
    
    Examples
    --------
    
    >>> from sssm.backend import Transaction
    >>> 
    """
    
    def __init__(self, stock, qty, price, 
                 timestamp=datetime.now(), user=None,
                 store=None, trade_type="BUY"):
    
        self._store = store if store else Store()
        if stock:
            self._stock = stock
        else:
            raise ValueError("[ERROR] Model: Stock symbol must be provided.")
        
        if qty:
            self._qty = qty 
        else:
            raise ValueError("[ERROR] Model: Stock quantity must be provided.")
            
        self._price = price if price else self._store['stocks'][self._stock]['Price']
        self._timestamp = timestamp
        self._trade_type = trade_type

        if user:
            self._user = user
        else:
            raise ValueError("[ERROR] Model: A trader must be provided.")

    @property    
    def user():
        return self._user
    
    @user.setter
    def user(self, user):
        self._user = user
        
    @property    
    def qty():
        return self._qty
    
    @qty.setter
    def qty(self, qty):
        self._qty = qty

    @property    
    def trade_type():
        return self._trade_type
    
    @trade_type.setter
    def trade_type(self, trade_type):
        self._trade_type = trade_type
        
    @property    
    def price():
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = price
        
    @property    
    def timestamp():
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @property    
    def stock():
        return self._stock
    
    @stock.setter
    def store(self, stock):
        self._stock = stock
        
    @property    
    def store():
        return self._store
    
    @store.setter
    def store(self, store):
        self._store = store
        
    def save(self):
        if self._user not in self._store.get_traders():
            return ValueError("[ERROR] Trade: User {} doesn't exist.".format(self._user))
        
        self._transaction_id = str(uuid.uuid3(
                                        uuid.NAMESPACE_DNS,
                                         str(self._timestamp) \
                                         + self._trade_type  \
                                         + str(self._price) \
                                         + self._user \
                                         + self._stock \
                                         + str(self._qty) 
                              ))
            
        self._value = self._qty * self._price
        
        logging.debug('[INFO] Platform: Recording trade {}'.format(self._transaction_id))
        
        self._record = {
                'trader': self._user,
                'id': self._transaction_id,
                'type': self._trade_type,
                'ts':  self._timestamp,
                'symbol' : self._stock,
                'volume' : self._qty,
                'value': self._value,
                'per_price': self._price
               }
        self._store['transactions'][self._transaction_id] = self._record
        
        return self._transaction_id
    
    def load(self, id):
        self._record = self._store['transactions'][id]
        self._load(self._record)
        
        return self._record
    
    def _load(self, record):
        self._user = record['trader']
        self._trade_type = record['type']
        self._timestamp = record['ts']
        self._stock = record['symbol']
        self._qty = record['volume']
        self._value = record['value']
        self._price = record['per_price']

class Stock(object):
    """ A Stock - Abstract record mapper and data access class for stocks.
    
    Examples
    --------
    See implementation examples.
    """
    
    def __init__(self, store=None):
        if store:
            self.store = store
        else:
            self.store = Store()
        
    @validate_stock('')
    def get_current_price(self, symbol):
        stock = self.store['stocks'][symbol]
        return stock['Price']
    
    @validate_stock('')
    def set_current_price(self, symbol, price):
        self.store['stocks'][symbol]['Price'] = price
    
    @validate_stock('')
    def get_last_dividend(self, symbol):
        return self.store['stocks'][symbol]['Last_Dividend']
    
    @validate_stock('')
    def get_par_value(self, symbol):
        return self.store['stocks'][symbol]['Par_Value']
    
class CommonStock(Stock):
    """ A Common Stock model - Record mapper and data access class for common stocks.
    
    Examples
    --------
    
    >>> from sssm.backend import CommonStock
    >>> symbol = 'TEA'
    >>> stock = CommonStock(symbol)
    >>> stock.get_current_price()
    13.0
    """
    
    def __init__(self):
        super(CommonStock, self).__init__()

class PreferredStock(Stock):
    """ A Preferred Stock model - Record mapper and data access class for preferred stocks.
    
    Examples
    --------
    
    >>> from sssm.backend import CommonStock
    >>> symbol = 'GIN'
    >>> stock = PreferredStock(symbol)
    >>> stock.get_current_price()
    13.0
    """
    
    def __init__(self, ):
        super(PreferredStock, self).__init__()
    
    @validate_stock('')
    def get_fixed_dividend(self, symbol):
        return self.store['stocks'][symbol]['Fixed_Dividend']