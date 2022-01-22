import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)
    sheet = client.open("stocks").sheet1
    sheet.append_row(['=GOOGLEFINANCE("GOOG", "price", DATE(2014,1,1), DATE(2014,12,31), "DAILY")'], value_input_option="USER_ENTERED")
    data = sheet.get_all_records()
    print(data)


if __name__ == "__main__":
    main()
