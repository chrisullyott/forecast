class Account:
    '''
    Implements a container of funds where an initial balance and annual ROI
    can be defined.
    '''
    def __init__(self, name, initial_balance, annual_return):
        self.name = str(name)
        self.principal = float(initial_balance)
        self.interest = 0
        self.annual_return = round(float(annual_return)/100, 10)

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
