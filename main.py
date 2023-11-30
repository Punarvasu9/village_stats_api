from fastapi import FastAPI
from typing import Optional
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return "For getting village stats add /village/village_id"

def get_data(village_id):
    url = 'https://www.onefivenine.com/village.dont?method=displayVillage&villageId=' + str(village_id)

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html')
    table = soup.find_all('table')[4]

    data = table.find_all('td')

    parameters = [val.text.strip() for val in data]

    col_name = []
    col_val = []

    parameters = parameters[2:]

    for i in range(len(parameters)):
        if i%2:
            col_val.append(parameters[i])
        else:
            col_name.append(parameters[i])

    return col_name, col_val

@app.get("/village/{village_id}")
def read_item(village_id: int):
    return get_data(village_id)