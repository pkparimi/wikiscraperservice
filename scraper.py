from bs4 import BeautifulSoup
import requests

article = input("What do you want?: ")
URL = f'https://en.wikipedia.org/wiki/{article}'

resp = requests.get(URL)

soup = BeautifulSoup(resp.text, 'html.parser')

article_dict = {}

toc = soup.find(id="toc")

p_before_toc = toc.find_all_previous("p")

description = ""

for p in p_before_toc:
    if not p.text.isspace():
        description = description + p.text + "\r\n"

print(description)