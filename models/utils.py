from models.user_item import Item
from typing import List


def calculate_cart_total(items: List[Item]):
    total = 0
    for item in items:
        total += item.price

    return float(total)


