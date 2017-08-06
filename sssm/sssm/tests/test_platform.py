import pytest
from datetime import datetime
from datetime import timedelta
import random
import uuid
import logging

import numpy as np

from sssm.backend import CommonStock, PreferredStock, Transaction, Store, Trader, Shares_Trading, Platform

def test_dividend():
    pass

def test_peratio():
    pass

def test_trading():
    timestamp = datetime.now()
    price = 15.0
    stock = 'TEA'
    trade_type = 'SELL'
    trader = 'trader1'
    qty = 1000
    s = Store()
    st = Shares_Trading(store=s)
    trader = 'trader1'
    
    td = Trader(trader, store=s)
    token = td.save()
    
    trader_init_qty = 0
    
    trader_portfolio = td.portfolio
    
    if len(trader_portfolio) > 0:
        for share in trader_portfolio:
            if share['symbol'] == stock:
                trader_init_qty = share['symbol']['qty']
        
    shares_init_qty = st.get_qty(stock)
    
    p = Platform(s)
    
    p.trade(trader, token, stock, qty, price)
    
    trader_portforlio = td.portfolio
    
    expected_portfolio = [{'symbol':stock, 'qty':qty, 'price': price}]
    
    if len(trader_portfolio) > 0:
        for share in trader_portfolio:
            if share['symbol'] == stock:
                trader_post_qty = share['qty']
                
    shares_post_qty = st.get_qty(stock)
    
    shares_qty_diff = shares_init_qty - 1000
    
    assert trader_post_qty == 1000
    assert st.get_qty(stock) == shares_qty_diff
    assert trader_portfolio == expected_portfolio
    
    # trader tries to sell some stock they don't have
    qty = 1001
    price = 15.5

    with pytest.raises(ValueError):
        p.trade(trader, token, stock, qty, price, trade_type='SELL')
    
    qty = 100000000
    price = 16.1
    
    # no sufficient stock to trade
    with pytest.raises(ValueError):
        p.trade(trader, token, stock, qty, price)
        
def test_volume_weighted_stock_price():
    base_price = 22.0
    stocks = ['TEA', 'GIN', 'JOE', 'ALE', 'POP']
    trade_types = ['SELL', 'BUY']
    s = Store()
    
    traders = []
    tokens = []
    
    for i in range(100):
        trader = uuid.uuid4()
        traders.append(str(trader))
        td = Trader(str(trader), store=s)
        tokens.append(td.save())
        
    
    # trading times: simulate 30mins of trading
    now = datetime.now()
    txn_times = [now - timedelta(seconds=i) for i in range(1800)]
    txn_ids = []
    
    p = Platform(s)
    
    for time in txn_times:
        idx = random.randint(0, 99)
        qty = random.randrange(1, 10000, 1)
        ttype_idx = random.randint(0, 1)
        stocks_idx = random.randint(0, 4)
        price = base_price + 10 * random.random()
        
        try:        
            txn_ids.append(p.trade(traders[idx], tokens[idx], stocks[stocks_idx], 
                qty, price, trade_type=trade_types[ttype_idx], timestamp=time))
                         
        except ValueError:
            pass
        
    price_qty = []
    qty = []
    
    logging.debug('[INFO] Model: Test2 {}'.format(len(txn_ids)))
    
    txn_orm = Transaction(None, None, stocks[0], store=s)
    
    valid_trades = txn_orm.find(txn_times[899])

    for txn_id in valid_trades:
        if txn_id:
            txn = txn_orm.load(txn_id)
            price_qty.append(txn['volume'] * txn['per_price'])
            qty.append(txn['volume'])
        
    volume_weighted_stock_price = sum(price_qty) / sum(qty)
    
    assert abs(p.volume_weighted_stock_price(since=15, time_ref=now) - volume_weighted_stock_price) < 0.05
    
    
    def test_all_share_index():
        base_price = 22.0
        stocks = ['TEA', 'GIN', 'JOE', 'ALE', 'POP']
        s = Store()
        p = Platform(s)
        
        for stock in stocks:
            # update stock price
            if s.get_type(symbol) == "Preferred":
                PreferredStock(self._store).set_current_price(symbol, base_price * random.random())
            else:
                CommonStock(self._store).set_current_price(symbol, base_price * random.random())
        
        shares_prices = [PreferredStock(s).get_current_price(symbol) \
                         if self._store.get_type(symbol) == 'Preferred' else \
                         CommonStock(s).get_current_price(symbol) for \
                         symbol in stocks \
                        ]
        
        shares_prices = np.array(shares_prices)
        
        assert shares_prices.prod()**(1.0/len(shares_prices)) == p.all_shares_index()
        
    def test_pe_ratio():
        
        symbol = 'TEA'
        price = 15.0
        s = Store()
        p = Platform(s)
        
        assert ps.pe_ratio(symbol, price) == CommonStock(s).pe_ratio(symbol, price)
        