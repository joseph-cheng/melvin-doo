import requests
from bs4 import BeautifulSoup


etfs = {
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
}

company_categories = {}

url = "https://www.marketwatch.com/investing/fund/%s/holdings"


for etf in etfs:
    print(etf)
    r = requests.get(url % etf)
    soup = BeautifulSoup(r.text, 'html.parser')
    holdings = soup.find("div", {"class":"holdings"})
    tickers = holdings.find_all('td', {"class": "u-semi"})
    for ticker in tickers:
        text = ticker.getText()
        if len(text.strip()) > 0 and text.upper() == text:
            if text not in company_categories:
                company_categories[text] = set()
            company_categories[text].add(etfs[etf])

for company in company_categories:
    print(company, company_categories[company])




