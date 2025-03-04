from playwright.sync_api import Page
from models.user_item import User

class Login:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.login_link = self.page.get_by_role("link", name="Log in")
        self.username_input = self.page.locator("#loginusername")
        self.password_input = self.page.locator("#loginpassword")
        self.login_button = self.page.get_by_role("button", name="Log in")
    

    def go_to(self):
        self.login_link.click()

    def login(self, user: User):
        self.username_input.fill(user.username)
        self.password_input.fill(user.password)
        self.login_button.click()