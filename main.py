import os
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# SHEETY IMPORTS
sheety_project_name = os.getenv("SHEETY_PROJECT_NAME")
sheety_project_sheet = os.getenv("SHEETY_PROJECT_SHEET")
sheety_app_key = os.getenv("SHEETY_API_KEY")
sheety_endpoint = f"https://api.sheety.co/{sheety_app_key}/{sheety_project_name}/{sheety_project_sheet}"
sheety_headers = {
    "Authorization": os.getenv("SHEETY_AUTH")
}

# Twilio API Config
twilio_accid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_authtoken = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(twilio_accid, twilio_authtoken)


class SendAlert:

    def send_sms(self, message):
        message = client.messages \
            .create(
            body=message,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=os.getenv("MY_PHONE_NUMBER")
        )
        print(message.status)

sheety_response = requests.get(url=sheety_endpoint, headers=sheety_headers)
sheety_data = sheety_response.json()
for item in sheety_data['items']:
    URL = item['url']
    desired_price = item['desiredPrice']
    response = requests.get(URL, headers={"User-Agent": os.getenv("USER_AGENT"), "Accept-Language": os.getenv("ACCEPT_LANGUAGE")})
    website_html = response.text
    soup = BeautifulSoup(website_html, "html.parser")
    price = soup.find(name="span", class_="a-price-whole")
    price = price.getText().replace('.', '')
    price = price.replace(',', '')
    price = int(price)
    if price < desired_price:
        message = f"Price dropped for {item['name']} from:- \n ₹{desired_price} to ₹{price}."
        send_alert = SendAlert()
        send_alert.send_sms(message=message)
        print(message)
