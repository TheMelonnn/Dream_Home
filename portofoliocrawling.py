import requests
from bs4 import BeautifulSoup
import gspread

def crawl_web_antam(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", class_="lm-table")

    if not table:
        print("Tabel tidak ditemukan")
        return None

    data_berat = []
    data_harga_jual = []
    data_harga_beli = []

    for row in table.select("tbody tr"):
        cols = row.find_all("td")
        if len(cols) != 3:
            continue

        # Berat
        berat = cols[0].find("a").get_text(strip=True)

        # Harga jual & beli
        harga_jual = cols[1].select("span span")[1].get_text(strip=True)
        harga_beli = cols[2].select("span span")[1].get_text(strip=True)

        harga_jual = int(harga_jual.replace(".", ""))
        harga_beli = int(harga_beli.replace(".", ""))

        data_berat.append(berat)
        data_harga_jual.append(harga_jual)
        data_harga_beli.append(harga_beli)

    return data_berat, data_harga_jual, data_harga_beli

def get_api_indodax():
    def get_price(pair):
        url = f"https://indodax.com/api/ticker/{pair}"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        return int(data["ticker"]["last"])
    
    pairs = {
    "BTC": "BTCIDR",
    "ETH": "ETHIDR",
    "BNB": "BNBIDR",
    "SOL": "SOLIDR",
    "DOGE": "DOGEIDR",
    "XRP": "XRPIDR",
    "LINK": "LINKIDR",
    # "PEPE": "PEPEIDR",
    "ADA": "ADAIDR",
    "POL": "POLIDR",
    # "SHIB": "SHIBIDR",
    "BOME": "BOMEIDR",
    # "PENGU": "PENGUIDR",
    # "DOGS": "DOGSIDR",
    "ALT": "ALTLAYERIDR"
    }

    prices = {}

    for coin, pair in pairs.items():
        prices[coin] = get_price(pair)
    
    return prices

def run_crawl():
    gc = gspread.service_account(filename="portofoliomanager-56b48bd00efa.json")

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1g4ikZC3Xr9AkKmaT4KHJ-NCGRszJv8d7e0LcAiMma54/edit"
    spreadsheet = gc.open_by_url(spreadsheet_url)

    worksheet = spreadsheet.worksheet("My Portofolio")

    data_berat, data_harga_jual, data_harga_beli = crawl_web_antam(
        "https://anekalogam.co.id/id"
    )

    rows = []
    for i in range(len(data_berat)):
        rows.append([
            f"Emas {data_berat[i]}",
            data_harga_jual[i],
            data_harga_beli[i]
        ])

    start_row = 4
    end_row = start_row + len(rows) - 1

    cell_range = f"C{start_row}:E{end_row}"


    worksheet.update(cell_range, rows)
    return True

def run_crawl_crypto():
    gc = gspread.service_account(filename="portofoliomanager-56b48bd00efa.json")

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1g4ikZC3Xr9AkKmaT4KHJ-NCGRszJv8d7e0LcAiMma54/edit"
    spreadsheet = gc.open_by_url(spreadsheet_url)

    worksheet = spreadsheet.worksheet("My Portofolio")

    prices = get_api_indodax()
    rows = [[name, price] for name, price in prices.items()]

    start_row = 12
    end_row = start_row + len(rows) - 1

    worksheet.update(f"C{start_row}:D{end_row}", rows)
    return True


