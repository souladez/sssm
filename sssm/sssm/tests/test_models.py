import pytest
from datetime import datetime

from sssm.backend import CommonStock, PreferredStock, Transaction, Store, Trader
from sssm.backend import data
import uuid

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
    
def test_stocks_access():
    
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

def test_traders_access():
    id = 'trader1'
    token = uuid.uuid4()
    s = Store()
    created = datetime.now()
    
    trader_record = {
                'id': id,
                'token': token,
                '_type': 'User',
                'created' : created
            }
    trader = Trader(id, token=token, store=s, created=created)
    
    trader.save()
    
    assert id in s.get_traders()
    assert trader.load(id) == trader_record
    
    with pytest.raises(ValueError):
        trader = Trader(None, token=token, store=s, created=created)
        
def test_trades_access():
    timestamp = datetime.now()
    price = 15.0
    stock = 'TEA'
    trade_type = 'SELL'
    qty = 1000
    s = Store()
    trader = 'trader1'
    
    td = Trader(trader, store=s)
    
    td.save()
    
    t = Transaction(stock, qty, price, 
                 timestamp=timestamp, user=trader,
                 store=s, trade_type=trade_type)
    
    expected_transaction_id = str(uuid.uuid3(
                                        uuid.NAMESPACE_DNS,
                                         str(timestamp) 
                                         + trade_type  
                                         + str(price) 
                                         + trader 
                                         + stock 
                                         + str(qty)
    ))
    
    txn_value = qty * price
    
    expected_txn = {
                'trader': trader,
                'id': expected_transaction_id,
                'type': trade_type,
                'ts':  timestamp,
                'symbol' : stock,
                'volume' : qty,
                'value': txn_value,
                'per_price': price
               }
    transaction_id = t.save()
    
    assert expected_transaction_id == transaction_id
    assert expected_transaction_id in s.get_transactions()
    assert t.load(transaction_id) == expected_txn
    
    with pytest.raises(ValueError):
        t = Transaction(None, qty, price, 
                 timestamp=timestamp, user=trader,
                 store=s, trade_type=trade_type)
    
    with pytest.raises(ValueError):
        t = Transaction(stock, None, price, 
                 timestamp=timestamp, user=trader,
                 store=s, trade_type=trade_type)
   
    with pytest.raises(ValueError):
        t = Transaction(stock, qty, price, 
                 timestamp=timestamp,
                 store=s, trade_type=trade_type)