from __future__ import absolute_import, division, print_function

from datetime import datetime
from datetime import timedelta
import random
import time

from tornado import gen
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import uuid

# load packages
from sssm.backend import (
    Store, 
    CommonStock, 
    PreferredStock, 
    Trader, 
    Transaction, 
    Shares_Trading,
    Platform
)

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/stock", StockHandler),
            (r"/stock/([^/]+)", StockHandler),
            (r"/platform/([^/]+)", PlatformHandler),
            (r"/platform", PlatformHandler),
            (r"/user", UserHandler),
        ]
        
        settings = dict(
            app_title=u"JP Morgan Super Simple Stock Market",
            xsrf_cookies=True,
            debug=True,
        )
        
        super(Application, self).__init__(handlers, **settings)

class IndexHandler(tornado.web.RequestHandler):
    def get(self, symbol=None):
        self.write("Welcome to JP Morgan Super Simple Stock Market.\
            Please see README.md for permitted operations. \
            Make sure to restart service every 30 mins as opertions would fail otherwise.")
    
class StockHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        pass
    
    def get(self, symbol=None):
        if symbol not in Store().get_shares_trading():
            self.write("Stock {} is not trading.".format(symbol))
        else:    
            s = Store()
            
            if self.get_argument("operation", None):
                operation = self.get_argument("operation", None)
                
                if self.get_argument("price", None):
                    price = self.get_argument("price", None)
                else:
                    self.write("Price must be provided for {}".format(operation))
                 
                if operation == "dividend":
                    if s.get_type(symbol) == "Preferred":
                        self.write(str(PreferredStock(s).dividend_yield(str(symbol), float(price))))
                    else:
                        self.write(str(CommonStock(s).dividend_yield(str(symbol), float(price))))
                elif operation == "peratio":
                    if s.get_type(symbol) == "Preferred":
                        self.write(str(PreferredStock(s).pe_ratio(str(symbol), float(price))))
                    else:
                        self.write(str(CommonStock(s).pe_ratio(str(symbol), float(price))))
                else:
                    self.write("API: Specified operation not supported.")
                    
            else:
                self.write("API: Operation must be provided")
                
class PlatformHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def post(self):
        pass
    
    def get(self, operation=None):
        if operation:
            if operation == "index":
                self.write(str(p.all_share_index()))
            elif operation == "volume_weighted_stock_price":
                self.write(str(p.volume_weighted_stock_price()))
        else:
            info = {
                "all_share_index": p.all_share_index(),
                "volume_weighted_stock_price": p.volume_weighted_stock_price()
            }
            self.write(info)
            
class UserHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def set_current_price(self):
        pass
    
    def get_current_price(self):
        pass
    
    def dividend_yield(self):
        pass
    
    def dividend_yield(self):
        pass

s = Store()
p = Platform(s)
p.simulate()

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()