from datetime import date
from datetime import datetime
from dateutil import relativedelta

def parse_month_string(string):
    return datetime.strptime(string, '%m-%Y').date()

def date_this_month_began():
    return date.today().replace(day=1)

def date_next_month_begins():
    delta = relativedelta.relativedelta(months=+1)
    return (date.today() + delta).replace(day=1)

def date_x_month_begins(months):
    delta = relativedelta.relativedelta(months=months)
    return (date_this_month_began() + delta).replace(day=1)
