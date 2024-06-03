from pybit.unified_trading import HTTP

def get_price():
    cl = HTTP()
    r = cl.get_orderbook(category='linear', symbol='NOTUSDT')
    return r['result'].get('b')[-1][0]

def compute_change_price(early_price, now_price):
    return round(now_price-early_price, 5)

price = [0, 0.1]
price_limit = [0.0, 0.0]

def notification_price(top_limit, bottom_limit):
    if float(get_price()) > top_limit:
        return 'top_limit'
    if float(get_price()) < bottom_limit:
        return 'bottom_limit'