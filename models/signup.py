from playwright.sync_api import Page, Route
from models.user_item import User 

class Signup:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.signup_link = self.page.get_by_role("link", name="Sign up")
        self.username_input = self.page.locator("#sign-username")
        self.password_input = self.page.locator("#sign-password")
        self.signup_button = self.page.locator("button", has_text="Sign up")
        self.password_hash = ""


    def go_to(self):
        self.signup_link.click()    


    def signup(self, user: User) -> str:
        self.page.route(
        "https://api.demoblaze.com/signup",
         self.get_hashed_password
        )

        self.username_input.fill(user.username)
        self.password_input.fill(user.password)
        self.signup_button.click()
        return self.password_hash

    def get_hashed_password(self, route: Route, user: User):
        self.password_hash = route.request.post_data_json['password']
        route.continue_()


