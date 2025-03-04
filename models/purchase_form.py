from playwright.sync_api import Page
from models.user_item import User
from typing import List


class PurchaseFrom:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.purchase_total = self.page.get_by_text("Total:")
        self.name_input = self.page.locator("#name")
        self.country_input = self.page.locator("#country")
        self.city_input = self.page.locator("#city")
        self.credt_card_input = self.page.locator("#card")
        self.month_input = self.page.locator("#month")
        self.year_input = self.page.locator("#year")
        self.purchase_btn = self.page.get_by_role("button", name="Purchase")

    def get_purchase_total(self):
        return self.purchase_total.inner_text().split()[1]

    def do_purchase(self, user: User):
        self.name_input.fill(user.name)
        self.country_input.fill(user.country)
        self.city_input.fill(user.city)
        self.credt_card_input.fill(user.credit_card)
        self.month_input.fill(user.month)
        self.year_input.fill(user.year)

        self.purchase_btn.click()


