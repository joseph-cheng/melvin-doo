import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# ARGS: name       - Stock symbol (eg. GOOG)
#       start      - Start date of price data
#       end        - End date of price data (both given as datetime objects)
#       resolution - Step size between data points (defaults to DAILY, can be set to WEEKLY)
#
# RETURN: A list of tuples of the date and the value the stock it traded for
def get_stock_data(ticker: str, start: datetime, end: datetime, resolution: str = "DAILY"):
    query = f'=GOOGLEFINANCE("***REMOVED***ticker***REMOVED***", "price", DATE(***REMOVED***start.year***REMOVED***,***REMOVED***start.month***REMOVED***,***REMOVED***start.day***REMOVED***), ' \
            f'DATE(***REMOVED***end.year***REMOVED***,***REMOVED***end.month***REMOVED***,***REMOVED***end.day***REMOVED***), "***REMOVED***resolution***REMOVED***")'
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)
    sheet = client.open("stocks").sheet1
    sheet.clear()
    sheet.append_row([query], value_input_option="USER_ENTERED")
    data = sheet.get_all_records()
    price_data = []
    for row in data:
        try:
            date_arr = [int(x) for x in row['Date'].split(' ')[0].split('/')]
            price_data.append((datetime.datetime(*list(reversed(date_arr))), row['Close']))
        except ValueError:
            print("Returning price data early")
            return price_data
    return price_data


if __name__ == "__main__":
    start = datetime.datetime(2019, 4, 20)
    end = datetime.datetime(2019, 7, 30)
    res = get_stock_data("TSLA", start, end)
