class Account:
    def __init__(self, id, initial_balance, annual_return):
        self.id = str(id)
        self.principal = float(initial_balance)
        self.interest = 0
        self.annual_return = round(float(annual_return)/100,10)

    def add(self, amount):
        self.principal += amount
        return self

    def compound(self, per_year):
        interest_rate = self.annual_return / per_year
        self.interest += self.get_balance() * (interest_rate)
        return self

    def get_principal(self):
        return round(self.principal, 2)

    def get_interest(self):
        return round(self.interest, 2)

    def get_balance(self):
        return round(self.principal + self.interest, 2)
