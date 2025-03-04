from playwright.sync_api import Page
from models.user_item import Item
from typing import List


class CartPage:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.cart_link = self.page.get_by_role("link", name="Cart")
        self.items = self.page.locator("tbody tr.success") 
        self.cart_total = self.page.locator("#totalp")
        self.place_order_btn = self.page.get_by_role("button", name="Place Order")
    

    def go_to(self):
        self.cart_link.click()

    def get_items_in_cart(self):
        self.items.last.wait_for()

        items = []
        for item in self.items.all():
            items.append(item.locator("td").nth(1).inner_text())
        
        return items


    def get_cart_total(self):
        self.cart_total.wait_for()
        return self.cart_total.inner_text()

    def place_order(self):
        self.place_order_btn.click()