import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(headers, url):
    body = {"long_url": url}
    response = requests.post(
        "https://api-ssl.bitly.com/v4/shorten",
        headers=headers,
        json=body
    )
    if response.ok:
        bitlink = response.json()["link"]
        return bitlink
    else:
        return "Provided url is incorrect"


def count_clicks(headers, bitlink):
    parsed_url = urlparse(bitlink)
    bitlink = f"{parsed_url.netloc}{parsed_url.path}"
    response = requests.get(
      f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary",
      headers=headers
    )
    if response.ok:
        return response.json()["total_clicks"]
    else:
        return "Page does not exist"


def is_bitlink(headers, url):
    parsed_url = urlparse(url)
    body = {"bitlink_id": f"{parsed_url.netloc}{parsed_url.path}"}
    response = requests.post(
        "https://api-ssl.bitly.com/v4/expand",
        headers=headers,
        json=body
    )
    return response.ok


def main():
    load_dotenv()
    bitlink_token = os.environ['BITLINK_TOKEN']
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url",
        help="Return bitlink from usual url, \
            return number of clicks from bitlink",
        type=str
    )
    url = parser.parse_args().url
    headers = {"Authorization": f"Bearer {bitlink_token}"}
    if is_bitlink(headers, url):
        print("Количество переходов по ссылке битли:",
              count_clicks(headers, bitlink=url))
    else:
        print(shorten_link(headers, url))


if __name__ == "__main__":
    main()
