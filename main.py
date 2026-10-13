import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

trading_client = TradingClient(api_key, secret_key, paper=True)
account = trading_client.get_account()

stock = str(input("what stock: "))
qty = input("qty: ")

market_order_data = MarketOrderRequest(
                    symbol=stock,
                    qty=qty,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )

market_order = trading_client.submit_order(
                order_data=market_order_data
               )