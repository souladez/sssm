import pytest
from datetime import datetime

from sssm.backend import Store

def test_errors():
    
    s = Store()
    
    pytest.raises(KeyError, lambda: s['users']['trader1'])
    pytest.raises(IndexError, lambda: s['key1','key2'])
    
    # define a collection
    c = {'key1':'value1', 'key2':'value2'}
    
    # test unsupported operation - adding new data
    with pytest.raises(ValueError):
        s['collection'] = c
        
    # test unsupported operation - deleting data
    with pytest.raises(ValueError):
        del s['transactions']
        
def test_traders_store():
    
    s = Store()
    
    # test user storage
    trader =  {'id':'trader1', 'token': 'dummytoken'}
    
    s['traders']['trader1'] = trader
    
    assert s['traders']['trader1']['id'] == "trader1"
    assert len(s.get_traders()) == 1
    
    del s['traders']['trader1']
    assert len(s.get_traders()) == 0

    
def test_transactions_store():
    
    s = Store()
    
    # test txn storage
    txn_time = datetime.now()
    a_transaction =  {'id':'xyz', 'user':'trader1', 'type': 'BUY',
                      'ts':txn_time, 'symbol': 'TEA', 'volume': 1000,
                      'price_per_unit': 13.0, 'value': 13 * 1000
                     }
    
    s['transactions']['xyz'] = a_transaction
    
    assert s['transactions']['xyz']['id'] == "xyz"
    assert len(s.get_transactions()) == 1
    
    del s['transactions']['xyz']
    assert len(s.get_transactions()) == 0
    
    
    
def test_shares_trading_store():
    
    s = Store()
    
    # pre-transaction (a BUY) on TEA shares. TEA brand start trading at 12, 000, 000
    assert s['shares_trading']['TEA'] == 12000000
    
    # simulate a transaction. TEA shares bought = 1000000
    qty = 1000000
    
    s['shares_trading']['TEA'] = s['shares_trading']['TEA'] - qty
    
    assert s['shares_trading']['TEA'] == 11000000
    
    # pre-transaction (a SELL) on GIN shares. GIN brand start trading at 8, 000, 000
    assert s['shares_trading']['GIN'] == 8000000
   
    # simulate a transaction. GIN shares bought = 100,000
    qty = 100000
    
    s['shares_trading']['GIN'] = s['shares_trading']['GIN'] - qty
    
    assert s['shares_trading']['GIN'] == 7900000
    
    assert len(s.get_shares_trading()) == 5
    
def test_portfolio_store():
    
    s = Store()
    
    trader =  {'id':'trader1', 'token': 'dummytoken', 'portfolio': {}}
    
    s['traders']['trader1'] = trader
    
    # buy some stuck 
    tea = {
        'TEA': {'qty': 10000, 'current_price': 13.0}
    }
    
    s['traders']['trader1']['portfolio'].update(tea)
    
    # buy more stocks
    
    gin = {
        'GIN': {'qty': 8000, 'current_price': 10.0}
    }
    
    s['traders']['trader1']['portfolio'].update(gin)
    
    # sell some TEA stock
    qty = 1000
    
    tea = s['traders']['trader1']['portfolio']['TEA']
    
    tea.update({'qty': tea['qty'] - qty})
    
    assert len(s['traders']['trader1']['portfolio']) == 2
    assert s['traders']['trader1']['portfolio']['TEA']['qty'] == 9000
    assert s['traders']['trader1']['portfolio']['GIN']['qty'] == 8000
    