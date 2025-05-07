from playwright.sync_api import APIRequestContext, Response
from models.user_item import Item

class API:

    def __init__(self, context: APIRequestContext, auth_token="") -> None:
        self.context = context
        self.auth_token = auth_token
    

    def login(self, username, password_hash) -> Response:
        response = self.context.post(
            "/login",
            data={
                "username": username,
                "password": password_hash
            }
        )
        return response
    
    def get_auth_token(self, response: Response) -> str:
        return response.json().split()[1]

    def add_to_cart(self, prod_id):
        response = self.context.post(
            "/addtocart",
            data={
                "cookie": self.auth_token,
                "prod_id": prod_id,
                "flag": True,
                "id": "27330f4a-6686-f7d6-1298-68e2f660fb91"
            }
        )
        return response
    
    def get_items_in_cart(self) -> list:
        items = []
        response = self.get_cart()

        if response.status == 200:
            response_body = response.json()
            for item in response_body["Items"]:
                items.append(item)

        return items
    

    def get_cart(self) -> Response:
        response = self.context.post(
            "/viewcart",
            data={
                "cookie": self.auth_token,
                "flag": True 
            }
        )
        return response
        
    def get_item_details(self, prod_id) -> dict:
        response = self.get_item(prod_id)

        response_body = response.json()
        return {"name": response_body["title"], 
                "price": response_body["price"],
                "id": response_body["id"]
                }


    def get_item(self, prod_id) -> Response:
        response = self.context.post(
            "/view",
            data={"id": prod_id}
        )
        return response
    