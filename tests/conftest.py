from models.user_item import User, Item
import pytest
from playwright.sync_api import Playwright, Page, APIRequestContext


@pytest.fixture(scope="module")
def user():
    return User("dfhbnsufljk", "lusha")

@pytest.fixture(scope="module")
def estore_page(playwright: Playwright):
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=200,
    )
 
    page = browser.new_page()
    page.goto("https://www.demoblaze.com/")

    return page


@pytest.fixture()
def items():
    return [Item("Nexus 6", 650, "phone"), Item("MacBook Pro", 1100, "laptop")]

@pytest.fixture
def api_context(playwright: Playwright) -> APIRequestContext:
    api_context = playwright.request.new_context(
        base_url="https://api.demoblaze.com/",
        extra_http_headers={'Content-Type': 'application/json'},
    )

    yield api_context
    
    api_context.dispose()

