from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests 
import re
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from tqdm.auto import tqdm

print("Checkpoint 0")
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

service = Service("/Users/panavshah/Desktop/Desktop - Panav’s MacBook Pro/chromedriver-mac-x64/chromedriver")
driver = webdriver.Chrome(service=service)

url = "https://www.tennisabstract.com/cgi-bin/leaders.cgi?f="

driver.get(url)
driver.implicitly_wait(10)
html = driver.page_source
# print(html)

with open("data/players_1.html", "w") as f:
    f.write(html)

service = Service("/Users/panavshah/Desktop/Desktop - Panav’s MacBook Pro/chromedriver-mac-x64/chromedriver")
driver = webdriver.Chrome(service=service)

url = "https://www.tennisabstract.com/cgi-bin/leaders.cgi?players=51-100"

driver.get(url)
driver.implicitly_wait(10)
html = driver.page_source
# print(html)

with open("data/players_2.html", "w") as f:
    f.write(html)

print("Checkpoint 1")


with open("data/players_1.html") as file:
    soup = BeautifulSoup(file, "html.parser")
table_players = soup.find(class_='tablesorter')
players_a = table_players.find_all('a')
players = []
ctr = 0
for player_a in players_a:
    if ctr % 2 == 0:
        players.append(player_a.get_text().replace(" ", ""))
    ctr += 1


with open("data/players_2.html") as file:
    soup = BeautifulSoup(file, "html.parser")
table_players = soup.find(class_='tablesorter')
players_a = table_players.find_all('a')
ctr = 0
for player_a in players_a:
    if ctr % 2 == 0:
        players.append(player_a.get_text().replace(" ", ""))
    ctr += 1

print("Checkpoint 2")


def get_webscrape_player_data(i, player):
    url = f"https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p={player}&f=ACareerqq"
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')
    with open(f"players_data/{i}_{player}.html", "w") as file:
        file.write(str(soup))

    # print(script_tag)

print("Checkpoint 3")


for i, player in enumerate(players):
    print(i, player)
    get_webscrape_player_data(i, player)