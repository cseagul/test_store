from playwright.sync_api import Page
from models.user_item import Item
import time
from typing import List

class ProductsPage:

    def __init__(self, page: Page) -> None:
        self.page = page
  
        self.home_link = self.page.get_by_role("link", name="Home")
        self.phones_link = self.page.get_by_role("link", name="Phones")
        self.laptops_link = self.page.get_by_role("link", name="Laptops")
        self.add_to_cart_button = self.page.get_by_role("link", name="Add to cart")


    def go_to(self):
        self.home_link.click()

    def add_items_to_cart(self, items: List[Item]):
        for item in items:
            time.sleep(0.5)
            if item.type == "phone":
                self.phones_link.click()
            elif item.type == "laptop":
                self.laptops_link.click()
            
            self.page.wait_for_selector(".card-block .card-title a", state="visible")
            item_link = self.page.locator(".card-block .card-title a", has_text=item.name)
            item_link.click()
            self.add_to_cart_button.click()
            self.go_to()








            
    

