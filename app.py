from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import config

app = Flask(__name__)


def fetch_data(address, website):
    if website.name == "Core":
        url = website.url + address + '&apikey=b4d33c1698e4446dbf0f05f520117a76'
        response = requests.get(url, headers=config.HEADER)
        jsonchik = response.json()
        balance_crypto = jsonchik['result']
        print(balance_crypto)
        if balance_crypto is None:
            usd_balance_text = "$0.00"
            balance_crypto_text = "0 CORE"
        else:
            balance_crypto_value = float(balance_crypto) * 10 ** -18
            balance_float = round(float(balance_crypto_value), 5)
            balance_crypto_text = f"{balance_float:.5f}  CORE"
            usd_balance_text = "$" + str(config.core_to_usd(balance_float))

        return usd_balance_text, balance_crypto_text

    else:
        url = website.url + address
        response = requests.get(url, headers=config.HEADER)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            if (website.name == "Binance") or (website.name == "Ethereum"):

                balance_dollars = soup.select_one(
                    "html body main section:nth-of-type(3) div:nth-of-type(2) div:nth-of-type(1) div div div:nth-of-type(3)")
                balance_crypto = soup.select_one(
                    "html body main section:nth-of-type(3) div:nth-of-type(2) div:nth-of-type(1) div div div:nth-of-type(2) div div")
                balance_dollars_text = balance_dollars.get_text(strip=True)
                balance_crypto_text = balance_crypto.get_text(strip=True)
                balance_value = float(balance_crypto_text.split(" ")[0])
                rounded_balance_value = round(balance_value, 5)
                unit = balance_crypto_text.split(" ")[1]
                rounded_balance_crypto_text = f"{rounded_balance_value} {unit}"

                return re.sub(r'\([^)]*\)', '', balance_dollars_text).strip().replace("BNB Value", "").replace("Eth Value",
                                                                                                           ""), rounded_balance_crypto_text

            elif website.name == "Zksynk":
                jsonchik = response.json()
                balances_dict = jsonchik['balances']
                balance_crypto = next(iter(balances_dict.values()), None)
                if balance_crypto:
                    balance_crypto_crypto = balance_crypto['token']['symbol']
                    balance_crypto_value = float(balance_crypto['balance']) * 10**-18
                    balance_float = round(float(balance_crypto_value), 5)
                    balance_crypto_text = f"{balance_float:.5f}  {balance_crypto_crypto}"

                    usd_balance_text = "$" + str(config.eth_to_usd(balance_float))
                else:
                    balance_crypto_text = "0 ETH"
                    usd_balance_text = "$0.00"

                return usd_balance_text, balance_crypto_text

            else:

                div_elements = soup.find_all('div', class_='col-md-8')
                div_text = [div.get_text().strip() for div in div_elements[:2]]

                cleaned_texts = [re.sub(r'\([^)]*\)', '', text).strip() for text in div_text]
                first_value = float(cleaned_texts[0].split(' ')[0])
                rounded_first_value = round(first_value, 5)
                rounded_first_value_with_name = f"{rounded_first_value:.5f} {cleaned_texts[0].split(' ', 1)[1]}"

                return [cleaned_texts[1].replace("Less Than ", ">"), rounded_first_value_with_name]
        else:
            return ["Error"]


@app.route('/checker', methods=['GET', 'POST'])
def index():
    addresses = []
    with open("accounts.txt", "r") as file:
        addresses = [line.strip() for line in file.readlines()]

    data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_data, address, website) for address in addresses for website in
                   config.WEBSITES]

        for i, address in enumerate(addresses):
            row = {"address": address}
            for j, website in enumerate(config.WEBSITES):
                result_index = i * len(config.WEBSITES) + j
                row[website.name] = futures[result_index].result()

            data.append(row)

    return render_template('index.html', websites=config.WEBSITES, data=data)


@app.route('/', methods=['GET', 'POST'])
def startPage():
    return render_template('start.html')


if __name__ == '__main__':
    app.run()
