class Account:
    def __init__(self, id, initial_balance, interest_rate):
        self.id = str(id)
        self.principal = float(initial_balance)
        self.interest = 0
        self.interest_rate = round(float(interest_rate)/100,10)

    def add(self, amount):
        self.principal += amount
        return self

    def compound(self):
        self.interest += self.get_balance() * (self.interest_rate/12)
        return self

    def get_principal(self):
        return round(self.principal, 2)

    def get_interest(self):
        return round(self.interest, 2)

    def get_balance(self):
        return round(self.principal + self.interest, 2)
