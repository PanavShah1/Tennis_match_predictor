import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json
from IPython.display import display
import pickle
from Player_class import Player
from datetime import datetime

start_time = datetime.now()
with open('players.pkl', 'rb') as f:
    players = pickle.load(f)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))










