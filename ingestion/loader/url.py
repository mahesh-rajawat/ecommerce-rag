import requests
from bs4 import BeautifulSoup

def load(url: str) -> str:
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    return soup.get_text(" ")