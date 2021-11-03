from bs4 import BeautifulSoup
import requests
import json
from scraperhelpers import find_by_key_dicts, table_of_content_creator

# article = input("What do you want?: ")
article = "Elephant"
URL = f'https://en.wikipedia.org/wiki/{article}'

resp = requests.get(URL)

soup = BeautifulSoup(resp.text, 'html.parser')

toc = soup.find(id="toc")
(article_dict, article_list) = table_of_content_creator(toc)

    
for i in range(len(article_list)-1):
    
    description = ""
    p_total = []
    cur = soup.find_all(string=article_list[i])[1:2][0].parent.parent
    next_stop = soup.find_all(string=article_list[i+1])[1:2][0].parent.parent
    while cur != next_stop:
        if cur.name == 'p':
            p_total.append(cur)
        cur = cur.next_sibling

    for p in p_total:
        if not p.text.isspace():  # to avoid taking blank paragraphs
            for sup in p("sup"):  # clears all wikipedia annotations
                sup.decompose()
            description = description + p.text + " "
            
    this_dict = find_by_key_dicts(article_list[i], article_dict)

    this_dict["info"] = description




# description section
p_before_toc = toc.find_all_previous("p")

description = ""

for p in p_before_toc:
    if not p.text.isspace():  # to avoid taking blank paragraphs
        for sup in p("sup"):  # clears all wikipedia annotations
            sup.decompose()
        description = p.text + " " + description

article_dict["info"] = description

print(json.dumps(article_dict, indent = 4))