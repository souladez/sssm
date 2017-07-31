from __future__ import absolute_import, division, print_function

from functools import wraps
from sssm.backend import Store

def validate_stock(*param):
    def stock_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """ func wrapper """
            if not isinstance(args[1], str):
                raise ValueError("SSSM - Stock: [ERROR] Invalid Symbol {} specified.".format(args[1]))
            
            if not args[0].store['stocks'].get(args[1]):
                raise ValueError("SSSM - Stock: [ERROR] Stock doesn't exist in database.") 
            
            if len(args) > 2 and type(args[2]) != float:
                raise ValueError("SSSM - Stock: [ERROR] Invalid Price {} specified.".format(args[2]))
                
            return func(*args, **kwargs)
        return wrapper
    return stock_decorator

class Stock(object):
    """ A Stock - Abstract Data Access Class for stocks.
    
    Examples
    --------
    See implementation examples.
    """
    
    def __init__(self):
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
    """ A Common Stock model - Instantiates Data Access objects for common stocks.
    
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
    """ A Preferred Stock model - Instantiates Data Access objects for preferred stocks.
    
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