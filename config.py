import random


class Website:
    def __init__(self, name, url):
        self.name = name
        self.url = url


WEBSITES = [
    Website("Polygon", "https://polygonscan.com/address/"),
    Website("Arbitrum", "https://arbiscan.io/address/"),
    Website("Fantom", "https://ftmscan.com/address/"),
    Website("Optimism", "https://optimistic.etherscan.io/address/"),
    Website("Base", "https://basescan.org/address/"),
    Website("ZkvemPolygon", "https://zkevm.polygonscan.com/address/")
]


def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.78 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    ]
    return random.choice(user_agents)


HEADER = {
    'User-Agent': generate_user_agent()
}