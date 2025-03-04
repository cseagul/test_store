import pytest
from playwright.sync_api import Playwright, Page, Route, APIRequestContext, expect
from models.signup import Signup
from models.login import Login
from models.user_item import User, Item
from models.products_page import ProductsPage
from models.cart_page import CartPage
from models.purchase_form import PurchaseFrom
from models.utils import calculate_cart_total
from typing import List

hash = ""
auth_token = ""

def get_hashed_password(route: Route, user: User):
    global hash 
    hash = route.request.post_data_json['password']
    route.continue_()

@pytest.fixture(scope="module")
def user():
    return User("newuser", "lusha")

@pytest.fixture(scope="module")
def estore_page(playwright: Playwright):
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=200,
    )
 
    page = browser.new_page()
    page.goto("https://www.demoblaze.com/")
    page.route(
        "https://api.demoblaze.com/signup",
         get_hashed_password
    )

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


def test_signup(estore_page: Page, user: User):
    signup = Signup(estore_page)
    signup.go_to()
    signup.signup(user)
    
    expect(estore_page.locator("#signInModal")).to_be_hidden()


def test_login(estore_page: Page, user):
    login = Login(estore_page)
    login.go_to()
    login.login(user)

    expect(estore_page.locator("#logInModal")).to_be_hidden()


def test_add_items_to_cart(estore_page: Page, items: List[Item]):
    products_page = ProductsPage(estore_page)
    products_page.add_items_to_cart(items)

    cart_page = CartPage(estore_page)
    cart_page.go_to()

    items_in_cart = cart_page.get_items_in_cart()
    sorted_items = sorted([i.name for i in items])

    assert len(items_in_cart) == len(items)
    
    for i, item in enumerate(sorted(items_in_cart)):
        assert item == sorted_items[i]

    assert float(cart_page.get_cart_total()) == calculate_cart_total(items)
 

def test_place_order(estore_page: Page, items: List[Item], user: User):
    cart_page = CartPage(estore_page)
    cart_page.go_to()
    cart_page.place_order()

    purchase_form = PurchaseFrom(estore_page)
    
    assert float(purchase_form.get_purchase_total()) == calculate_cart_total(items)

    purchase_form.do_purchase(user)

    expect(estore_page.locator(".sweet-alert")).to_be_visible()


def test_api_login(api_context: APIRequestContext, user: User):
    response = api_context.post(
        "/login",
        data={
            "username": user.username,
            "password": hash
        }
    )
    assert response.status == 200
    
    global auth_token
    auth_token = response.json().split()[1]


def test_api_add_to_cart(api_context: APIRequestContext):
    response = api_context.post(
        "/addtocart",
        data={
            "cookie": auth_token,
            "prod_id": 3,
            "flag": True,
            "id": "27330f4a-6686-f7d6-1298-68e2f660fb91"
        }
    )
    assert response.status == 200


def test_validate_cart(api_context: APIRequestContext):
    response = api_context.post(
        "/viewcart",
        data={
           "cookie": auth_token,
           "flag": True 
        }
    )
    assert response.status == 200

    response_body = response.json()
    items_in_cart = len(response_body["Items"])
    prod_id = response_body["Items"][0]["prod_id"]

    assert items_in_cart == 1
    assert prod_id == 3

    response = api_context.post(
        "/view",
       data={"id": prod_id}
    )
    assert response.status == 200

    response_body = response.json()
    name = response_body["title"]
    price = response_body["price"]
    id = response_body["id"]
 
    assert name == "Nexus 6"
    assert price == float(650)
    assert id == 3
