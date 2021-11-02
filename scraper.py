from bs4 import BeautifulSoup
import requests

article = input("What do you want?: ")
URL = f'https://en.wikipedia.org/wiki/{article}'

resp = requests.get(URL)

soup = BeautifulSoup(resp.text, 'html.parser')

article_dict = {}

toc = soup.find(id="toc")

# description section
p_before_toc = toc.find_all_previous("p")

description = ""

for p in p_before_toc:
    if not p.text.isspace():  # to avoid taking blank paragraphs
        for sup in p("sup"):  # clears all wikipedia annotations
            sup.decompose()
        description = p.text + "\r\n" + description

article_dict["description"] = description

thissoup = toc.find_all_next(string="Etymology")[1]

nextsoup = toc.find_all_next(string="History")[1]

p_after = thissoup.find_all_next("p")
p_before = nextsoup.find_all_previous("p")

p_total = []

for p in p_after:
    if p in p_before:
        p_total.append(p)
        

print("done")