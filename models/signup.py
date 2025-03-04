from playwright.sync_api import Page
from models.user_item import User 

class Signup:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.signup_link = self.page.get_by_role("link", name="Sign up")
        self.username_input = self.page.locator("#sign-username")
        self.password_input = self.page.locator("#sign-password")
        self.signup_button = self.page.locator("button", has_text="Sign up")


    def go_to(self):
        self.signup_link.click()    

    def signup(self, user: User):
        self.username_input.fill(user.username)
        self.password_input.fill(user.password)
        self.signup_button.click()



