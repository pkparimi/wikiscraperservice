from bs4 import BeautifulSoup
import requests
import pprint
from scraperhelpers import find_by_key, table_of_content_creator

# article = input("What do you want?: ")
article = "USA"
URL = f'https://en.wikipedia.org/wiki/{article}'

resp = requests.get(URL)

soup = BeautifulSoup(resp.text, 'html.parser')

toc = soup.find(id="toc")

article_dict = table_of_content_creator(toc)


# description section
p_before_toc = toc.find_all_previous("p")

description = ""

for p in p_before_toc:
    if not p.text.isspace():  # to avoid taking blank paragraphs
        for sup in p("sup"):  # clears all wikipedia annotations
            sup.decompose()
        description = p.text + "\r\n" + description

article_dict["description"] = description

