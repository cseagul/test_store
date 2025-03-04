class User:

    def __init__(self, username="Assaf", password="Lusha", name="Yoni", 
                 country="Israel", city="Jerusalem", credit_card="324523",
                 month="03", year="24"
                ) :
        self.username = username
        self.password = password
        self.name = name
        self.country = country
        self.city = city
        self.credit_card = credit_card
        self.month = month
        self.year = year


class Item:
    def __init__(self, name, price, prod_type):
        self.name = name
        self.price = price
        self.type = prod_type



