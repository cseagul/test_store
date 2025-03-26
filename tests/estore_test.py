import pytest
from playwright.sync_api import Playwright, Page, Route, APIRequestContext, expect
from models.signup import Signup
from models.login import Login
from models.user_item import User, Item
from models.products_page import ProductsPage
from models.cart_page import CartPage
from models.purchase_form import PurchaseFrom
from models.utils import calculate_cart_total
from api.api import API
from typing import List

hash = ""
auth_token = ""

def get_hashed_password(route: Route, user: User):
    global hash 
    hash = route.request.post_data_json['password']
    route.continue_()

def test_signup(estore_page: Page, user: User):
    estore_page.route(
        "https://api.demoblaze.com/signup",
         get_hashed_password
    )

    global hash 
    signup = Signup(estore_page)
    signup.go_to()
    hash = signup.signup(user)

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
    api = API(api_context)

    response = api.login(user.username, hash)
    assert response.status == 200
    
    global auth_token
    auth_token = api.get_auth_token(response)


def test_api_add_to_cart(api_context: APIRequestContext):
    api = API(api_context, auth_token)
    response = api.add_to_cart(3)

    assert response.status == 200


def test_validate_cart(api_context: APIRequestContext):
    api = API(api_context, auth_token)
    items_in_cart = api.get_items_in_cart()

    prod_id = items_in_cart[0]["prod_id"]

    assert len(items_in_cart) == 1
    assert prod_id == 3

    item = api.get_item_details(prod_id)  
 
    assert item["name"] == "Nexus 6"
    assert item["price"] == float(650)
    assert item["id"] == 3
