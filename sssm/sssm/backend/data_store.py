from __future__ import absolute_import, division, print_function

from collections import defaultdict, MutableMapping
from sssm.backend import data

class Store(MutableMapping):
    """ Store - In-memory store for Super Simple Stock Market.
    
        The following stocks and trading data are accessed:
        ``stocks``, ``transactions``, ``traders``, ``trades``,
        ``shares_trading``.
        
    Examples
    --------
    Store data like a dictionary
    >>> from sssm.backend import Store
    >>> s = Store()
    >>> s['traders']['xyz'] = {'id':'xyz', 'token': 'token'} # add a new trader
    >>> s['traders']['xyz']
    {'token': 'token', 'id': 'xyz'}
    
    """
    
    def __init__(self, stocks=None, shares_trading=None):
        """ In-memory store setup.
        
        Parameters
        ----------
        stocks : list
            array of stock symbols
        shares_trading : dict
            Record mapper for shares trading
            
        """
        
        if stocks and type(stocks) == dict:
            self.stocks = stocks
        else:
            self.stocks = data.STOCKS
            
        if shares_trading and type(shares_trading) == dict:
            self.shares_trading = shares_trading
        else:
            self.shares_trading = data.SHARES_TRADING
            
        self.data = dict()
        self.keys = set()
        self.transactions = {}
        self.initialise_store()
    
    def initialise_store(self):
        """ Store initialiser - sets up Super Simple Stock Market data in
            ``sssm.backend.data``
        
        """
        
        self.transactions = {}
        self.traders = {}
        self.portfolio = {}
        
        self.data['stocks'] = self.stocks
        self.data['transactions'] = self.transactions
        self.data['portfolio'] = self.portfolio
        self.data['shares_trading'] = self.shares_trading
        self.data['traders'] = self.traders
            
    def __setitem__(self, key, value):
        raise ValueError("Super Simple Stock Market Store does not support addition of new items.")
        
    def __getitem__(self, key):
        """ Retrieve data from storage in dict-style format.
        
        Parameter
        ---------
        key : str
            data to retrive from store: 

        Returns
        -------
        self.data : dict or list
            requested data - one of stocks, traders, shares_trading, 
            transactions,
            
        """

        if not isinstance(key, str):
            raise IndexError("Store: Invalid key type specified.")
        
        if key not in data.COLLECTIONS:
            raise KeyError("Store: [ERROR] Collection {} does not exist.".format(key))
        
        if key is "traders":
            return self.data["traders"]

        if key is "transactions":
            return self.data["transactions"]
        
        if key is "shares_trading":
            return self.data["shares_trading"]
        
        if key is "portfolio":
            return self.data["portfolio"]
        
        if key is "stocks":
            return self.data["stocks"]
        
    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __delitem__(self, key):
        raise ValueError("Super Simple Stock Market Store does not support deletion.")
        
    def get_traders(self):
        return self.data['traders'].keys()

    def get_transactions(self):
        return self.data['transactions'].keys()
    
    def get_shares_trading(self):
        shares_trading = list()
        
        for share, volume in self.data['shares_trading'].items():
            if volume > 0:
                shares_trading.append(share)
                
        return shares_trading
    
    def get_type(self, symbol):
        """ Obtain stock type - Common or Preferred.
        
        Parameters
        ----------
        symbol : str
            stock symbol for which type is being requested.
            
        """
        
        return self.data['stocks'][symbol]['Type']
                