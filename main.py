import os
from decimal import Decimal
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass, OrderSide, TimeInForce, QueryOrderStatus
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, GetOrdersRequest, GetAssetsRequest

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

trading_client = TradingClient(api_key, secret_key, paper=True)

def market_order(symbol, qty, side, time_in_force=TimeInForce.DAY):
    market_order_data = MarketOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side=side,
                        time_in_force=time_in_force
                        )

    order = trading_client.submit_order(
                    order_data=market_order_data
                )
    return market_order

def limit_order(symbol, limit_price, notional, side, time_in_force=TimeInForce.DAY):
    limit_order_data = LimitOrderRequest(
                        symbol=symbol,
                        limit_price=limit_price,
                        notional=notional,
                        side=side,
                        time_in_force=time_in_force 
                    )
    order = trading_client.submit_order(
                    order_data=limit_order_data
                )
    return order

def get_orders(status, side):
    request_data = GetOrdersRequest(
                    status=status,
                    side=side
                )
    
    orders = trading_client.get_orders(filter=request_data)
    
    return orders

def get_finances():
    account = trading_client.get_account()
    equity = Decimal(account.equity)
    positions = trading_client.get_all_positions()
    unrealised_pl = sum(Decimal(position.unrealized_pl) for position in positions)
    total_position_value = sum(Decimal(position.market_value) for position in positions)
    return {
            "equity": equity,
            "unrealised_pl": unrealised_pl,
            "total_position_value": total_position_value
            }

def get_allocation(symbol):
    account = trading_client.get_account()  
    equity = Decimal(account.equity)
    position = trading_client.get_open_position(symbol)
    allocation = Decimal(position.market_value)/Decimal(equity)
    return allocation

stock = str(input("what stock: "))
qty = input("qty: ")
sideInput= input("buy or sell: ")
if sideInput.lower() == "sell": 
    side = OrderSide.SELL
else: 
    side = OrderSide.BUY
    
market_order(stock, qty, side)
position_test = trading_client.get_all_positions()
order_test = get_orders(QueryOrderStatus.ALL, OrderSide.BUY)
print("---POSITION---------------------------")
print(position_test)
print("---ORDER------------------------------")
print(order_test)
print("--------------------------------------")
trading_client.cancel_orders()
position_test = trading_client.get_all_positions()
order_test = get_orders(QueryOrderStatus.ALL, OrderSide.BUY)
print("---POSITION---------------------------")
print(position_test)
print("---ORDER------------------------------")
print(order_test)
print("--------------------------------------")