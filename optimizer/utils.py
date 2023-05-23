import json
from fastapi.encoders import jsonable_encoder
from factory import Order
def save_orders(orders):
    ord_enc = jsonable_encoder(orders)
    with open("orders.json", "w") as f:
        json.dump(ord_enc, f)

def load_order_sample():
    with open('optimizer/orders.json', 'r') as f:
        order_sample = json.load(f)
        return [Order(**order) for order in order_sample]
    