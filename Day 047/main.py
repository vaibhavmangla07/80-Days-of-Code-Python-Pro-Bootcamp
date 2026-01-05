from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv
import re

load_dotenv()

url = "https://www.amazon.com/dp/B075CYMYK6?psc=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

price_tag = soup.find(class_="a-offscreen")
if not price_tag:
    raise Exception("Price not found. Amazon may have blocked the request.")

price = price_tag.get_text()
price_as_float = float(re.sub(r"[^\d.]", "", price))

title = soup.find(id="productTitle").get_text(strip=True)

BUY_PRICE = price_as_float + 1  # testing

if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"

    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], 587) as connection:
        connection.starttls()
        connection.login(
            os.environ["EMAIL_ADDRESS"],
            os.environ["EMAIL_PASSWORD"]
        )
        connection.sendmail(
            from_addr=os.environ["EMAIL_ADDRESS"],
            to_addrs=os.environ["EMAIL_ADDRESS"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}"
        )
