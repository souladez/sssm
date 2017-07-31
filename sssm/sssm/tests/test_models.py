import pytest
from datetime import datetime

from sssm.backend import CommonStock, PreferredStock
from sssm.backend import data

#@pytest.mark.skip()
def test_errors():
    symbol1 = ['TEA', 'POP']
    symbol2 = 'PON'
    
    common = CommonStock()    
    preferred = PreferredStock()    
    
    with pytest.raises(ValueError):
        common.get_current_price(symbol1)
 
    with pytest.raises(ValueError):
        common.get_current_price(symbol2)
    
def test_ro_data_access():
    
    symbol1 = 'TEA'
    symbol2 = 'POP'
    symbol3 = 'ALE'
    symbol4 = 'GIN'
    symbol5 = 'JOE'
    
    common = CommonStock()    
    preferred = PreferredStock()      
    
    assert common.get_current_price(symbol1) == data.STOCKS[symbol1]['Price']
    assert common.get_current_price(symbol2) == data.STOCKS[symbol2]['Price']
    assert common.get_current_price(symbol3) == data.STOCKS[symbol3]['Price']
    assert preferred.get_current_price(symbol4) == data.STOCKS[symbol4]['Price']
    assert common.get_current_price(symbol5) == data.STOCKS[symbol5]['Price']
    
    assert preferred.get_last_dividend(symbol4) == data.STOCKS[symbol4]['Last_Dividend']
    assert common.get_last_dividend(symbol5) == data.STOCKS[symbol5]['Last_Dividend']
    
    assert preferred.get_par_value(symbol4) == data.STOCKS[symbol4]['Par_Value']
    assert common.get_par_value(symbol5) == data.STOCKS[symbol5]['Par_Value']
    
    assert preferred.get_fixed_dividend(symbol4) == data.STOCKS[symbol4]['Fixed_Dividend']
    
    tea_stock_price = 10.0
    gin_stock_price = 14.0
    
    common.set_current_price(symbol1, tea_stock_price)
    preferred.set_current_price(symbol4, gin_stock_price)
    
    assert common.get_current_price(symbol1) == tea_stock_price
    assert preferred.get_current_price(symbol4) == gin_stock_price

    
    