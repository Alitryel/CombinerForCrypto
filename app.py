from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import config

app = Flask(__name__)

def fetch_data(address, website):
    url = website.url + address
    response = requests.get(url, headers=config.HEADER)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        div_elements = soup.find_all('div', class_='col-md-8')
        div_text = [div.get_text().strip() for div in div_elements[:2]]

        cleaned_texts = [re.sub(r'\([^)]*\)', '', text).strip() for text in div_text]
        first_value = float(cleaned_texts[0].split(' ')[0])
        rounded_first_value = round(first_value, 5)
        rounded_first_value_with_name = f"{rounded_first_value:.5f} {cleaned_texts[0].split(' ', 1)[1]}"

        return [cleaned_texts[1], rounded_first_value_with_name]
    else:
        return ["Error"]


@app.route('/checker', methods=['GET', 'POST'])
def index():
    addresses = []
    with open("accounts.txt", "r") as file:
        addresses = [line.strip() for line in file.readlines()]

    data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_data, address, website) for address in addresses for website in config.WEBSITES]

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
