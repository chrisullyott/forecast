from datetime import date, datetime
from dateutil import relativedelta

def parse_date(date):
    date = str(date)
    date = '01-' + date if len(date) == 4 else date
    return datetime.strptime(date, '%m-%Y').date()

def date_this_month_began():
    return date.today().replace(day=1)

def date_this_year_began():
    return date.today().replace(day=1, month=1)

def date_x_month_begins(months):
    delta = relativedelta.relativedelta(months=months)
    return (date_this_month_began() + delta).replace(day=1)

def date_x_year_begins(years):
    delta = relativedelta.relativedelta(years=years)
    return (date_this_year_began() + delta).replace(day=1, month=1)
