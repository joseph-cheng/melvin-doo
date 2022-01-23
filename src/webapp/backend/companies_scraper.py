import requests
from bs4 import BeautifulSoup


def get_ticker_categories():

    categories = []

    etfs = ***REMOVED***
            "XLE": "energy",
            "XLF": "finance",
            "XLU": "utilities",
            "XLI": "industrial",
            "GDX": "precious metals",
            "XLK": "technology",
            "XLV": "health",
            "XLY": "retail",
            "XLP": "retail",
            "XLB": "materials",
            "XOP": "oil",
            "IYR": "real estate",
            "XHB": "real estate",
            "ITB": "real estate",
            "VNQ": "real estate",
            "GDXJ": "precious metals",
            "IYE": "energy",
            "OIH": "oil",
            "XME": "precious metals",
            "XRT": "retail",
            "SMH": "technology",
            "IBB": "technology",
            "KBE": "finance",
            "KRE": "finance",
            "XTL": "telecom",
    ***REMOVED***

    company_categories = ***REMOVED******REMOVED***

    url = "https://www.marketwatch.com/investing/fund/%s/holdings"

    for etf in etfs:
        r = requests.get(url % etf)
        soup = BeautifulSoup(r.text, 'html.parser')
        holdings = soup.find("div", ***REMOVED***"class":"holdings"***REMOVED***)
        tickers = holdings.find_all('td', ***REMOVED***"class": "u-semi"***REMOVED***)
        for ticker in tickers:
            text = ticker.getText()
            if len(text.strip()) > 0 and text.upper() == text:
                if text not in company_categories:
                    company_categories[text] = set()
                company_categories[text].add(etfs[etf])

    for company in company_categories:
        categories.append((company, company_categories[company]))

    return categories


if __name__ == "__main__":
    print(get_ticker_categories())

