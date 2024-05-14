import datetime


# name related
def parse_bank_name(url: str) -> str:
    """Method for parse URL and get Bank name"""
    return url.split("?")[0].split("/")[-1].split(".")[0]


# price related
def parse_rate(rate: str) -> tuple[str, float]:
    """Method for parse rate price and it's difference"""
    price = rate.split()[0].replace('.', '').replace(',', '.')
    diff = rate.split("(")[1].split(')')[0].replace('+', '').replace(',', '.') if rate.find('(') >= 0 else 0

    return (price, float(diff))

def parse_price_rate(rate: str | None) -> str | None:
    """Method for parse price rate"""
    return rate.replace('.', '').replace(',', '.') if isinstance(rate, str) and rate.find('.') >= 0 else None


# date related
def parse_date(date: str) -> str:
    """Method for parse date from string"""
    return date.split()[1]

def parse_time(date: str) -> str:
    """Method for parse time from string"""
    return date.split()[2]

def parse_date_time(date_str: str) -> float:
    """Method for parse date and time to epoch time"""
    date = parse_date(date_str)
    time = parse_time(date_str)

    return datetime.datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M").timestamp()
