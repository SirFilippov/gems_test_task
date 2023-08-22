from django.test import TestCase
import requests

from gems.settings import BASE_DIR


def send_csv():
    api = 'http://127.0.0.1:8000/api/v1/general'
    csv_path = BASE_DIR / 'deals.csv'
    # csv_path = BASE_DIR / 'pipka.txt'
    with open(csv_path, 'rb') as csvfile:
        files = {'file': csvfile}
        response = requests.post(api, files=files)

    print(response.text)


send_csv()
