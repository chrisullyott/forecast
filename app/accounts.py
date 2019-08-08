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

    def format_usd(self, number):
        return '${:,.2f}'.format(number)

    def get_principal(self, usd=False):
        return self.format_usd(self.principal) if usd else self.principal

    def get_interest(self, usd=False):
        return self.format_usd(self.interest) if usd else self.interest

    def get_balance(self, usd=False):
        balance = self.principal + self.interest
        return self.format_usd(balance) if usd else balance
