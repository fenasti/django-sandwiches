import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

# Define the base directory of the project (where manage.py is)
BASE_DIR = Path(__file__).resolve().parent.parent  # Adjust as needed

# Construct full path to creds.json
CREDS_PATH = BASE_DIR / 'creds.json'

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials using full path
CREDS = Credentials.from_service_account_file(CREDS_PATH)
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def validate_data(values):
    """
    Converts all string values into integers.
    Returns True if exactly 6 integers are provided, otherwise False.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            return False
    except ValueError:
        return False
    return True


def update_worksheet(data, worksheet):
    """
    Appends a row of data to the given worksheet.
    """
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus for each item.
    Positive = waste, Negative = extra made.
    """
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects last 5 entries of each item from sales worksheet.
    Returns a list of lists.
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculates average stock per item and adds 10%.
    Returns a list of rounded integers.
    """
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data