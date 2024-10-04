# portfolio/utils.py

import logging

import requests
from bs4 import BeautifulSoup


def fetch_stock_symbols():
    logging.info("Fetching stock symbols")
    url = "https://dps.psx.com.pk/market-watch"
    response = requests.get(url, timeout=100)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    data = {}

    # Parse the HTML to extract stock symbols and names
    # (Implementation depends on the actual HTML structure)
    cells = soup.find_all("tr")
    for cell in cells[1:]:
        td_element = cell.find_all("td")
        if "KSE100" in td_element[2].get_text():
            name = td_element[0].find("a").get("data-title")
            symbol = td_element[0].find("strong").get_text()
            price = float(td_element[7].get_text().replace(",", ""))
            shares = get_outstanding_shares(symbol)
            data[symbol] = {
                "name": name,
                "price": price,
                "shares": shares,
                "market_cap": price * shares,
            }
    logging.info(f"Fetched {len(data)} stock symbols")  # noqa: G004
    return data


def get_outstanding_shares(symbol):
    logging.info(f"Fetching outstanding shares for {symbol}")  # noqa: G004
    url = f"https://dps.psx.com.pk/company/{symbol}"
    response = requests.get(url, timeout=100)
    soup = BeautifulSoup(response.content, "html.parser")
    stat_items = soup.find_all("div", class_="stats_item")
    for item in stat_items:
        try:
            label_div = item.find("div", class_="stats_label")
            label_text = label_div.get_text(strip=True)
            if label_text == "Shares":
                value_div = item.find("div", class_="stats_value")
                market_cap = value_div.get_text(strip=True)
                logging.info(f"Outstanding shares for {symbol}: {market_cap}")  # noqa: G004
        except AttributeError:
            logging.exception(f"Could not find outstanding shares for {symbol}")  # noqa: G004
            continue
    return float(market_cap.replace(",", ""))
