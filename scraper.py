from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, article) -> None:
        self.article = article
        self.article_dict = {}
        self.article_list = []

        URL = f'https://en.wikipedia.org/wiki/{self.article}'
        
        resp = requests.get(URL)
        
        self.soup = BeautifulSoup(resp.text, 'html.parser')
    
    def table_of_content_creator(self):
        toc_soup = self.soup.find(id="toc")
        breaker = False
        level = 1
        section = 1
        level_stack = []  # stack to traverse nested keys
        cur_dict = self.article_dict

        while not breaker:
            cur_bullet = toc_soup.select('li[class*="tocsection-' + str(section) + '"]')[0]  # gets current TOC list item tag object
            section_text = cur_bullet.select(".toctext")[0].text # gets text of TOC list item
            
            if section_text in ("See also", "See Also", "Notes", "References"):
                self.article_list.append(section_text)
                break
            
            cur_level = int(cur_bullet['class'][0][9])

            if cur_level == level:
                if not level_stack:
                    self.article_dict[section_text] = None
                    self.article_list.append(section_text)
                    cur_dict = self.article_dict
                    level_stack.append(section_text)
                else:
                    level_stack.pop()
                    cur_dict[section_text] = None
                    self.article_list.append(section_text)
                    level_stack.append(section_text)
            elif cur_level > level:
                level = cur_level
                if not cur_dict[level_stack[-1]]:
                    cur_dict[level_stack[-1]] = {}
                    cur_dict = cur_dict[level_stack[-1]]
                cur_dict[section_text] = None
                self.article_list.append(section_text)
                level_stack.append(section_text)
            elif cur_level < level:
                num_to_pop = level - cur_level + 1
                level = cur_level
                for i in range(num_to_pop):
                    if level_stack:
                        level_stack.pop()
                if not level_stack:
                    self.article_dict[section_text] = None
                    self.article_list.append(section_text)
                    cur_dict = self.article_dict
                    level_stack.append(section_text)
                else:
                    cur_dict = self.toc_find_by_key(level_stack.pop(), self.article_dict)
                    cur_dict[section_text] = None
                    self.article_list.append(section_text)
                    level_stack.append(section_text)
                    
            section += 1
        return self.article_dict, self.article_list
    
    def toc_find_by_key(self, value, dic):
        # iterates through nested dictionary to find key 
        if value in dic:
            return dic[value]
        for v in dic.values():
            if isinstance(v, dict):
                if v != {}:
                    return self.toc_find_by_key(value, v)
        return None
    
    def dict_find_by_key(self, value, dic):
        # iterates through nested dictionary to find key 
        if value in dic:
            if dic[value] is None:
                dic[value] = {}
            return dic[value]
        for v in dic.values():
            if isinstance(v, dict):
                nested_dict = self.dict_find_by_key(value, v)
                if nested_dict is not None:
                    return nested_dict
                
    def article_text_retriever(self):
        for i in range(len(self.article_list)-1):
            description = ""
            p_total = []
            cur = self.soup.find_all(string=self.article_list[i])[1:2][0].parent.parent
            next_stop = self.soup.find_all(string=self.article_list[i+1])[1:2][0].parent.parent
            
            while cur != next_stop:
                if cur.name == 'p':
                    p_total.append(cur)
                cur = cur.next_sibling

            for p in p_total:
                if not p.text.isspace():  # to avoid taking blank paragraphs
                    for sup in p("sup"):  # clears all wikipedia annotations
                        sup.decompose()
                    description = description + p.text + " "
                    
            this_dict = self.dict_find_by_key(self.article_list[i], self.article_dict)

            this_dict["info"] = description
        
        toc_soup = self.soup.find(id="toc")
        p_before_toc = toc_soup.find_all_previous("p")
        pre_toc_description = ""

        for p in p_before_toc:
            if not p.text.isspace():  # to avoid taking blank paragraphs
                for sup in p("sup"):  # clears all wikipedia annotations
                    sup.decompose()
                pre_toc_description = p.text + " " + pre_toc_description

        self.article_dict["info"] = pre_toc_description

# # article = input("What do you want?: ")
# article = "Elephant"
# URL = f'https://en.wikipedia.org/wiki/{article}'

# resp = requests.get(URL)

# soup = BeautifulSoup(resp.text, 'html.parser')

# toc = soup.find(id="toc")
# (article_dict, article_list) = table_of_content_creator(toc)

    
# for i in range(len(article_list)-1):
    
#     description = ""
#     p_total = []
#     cur = soup.find_all(string=article_list[i])[1:2][0].parent.parent
#     next_stop = soup.find_all(string=article_list[i+1])[1:2][0].parent.parent
#     while cur != next_stop:
#         if cur.name == 'p':
#             p_total.append(cur)
#         cur = cur.next_sibling

#     for p in p_total:
#         if not p.text.isspace():  # to avoid taking blank paragraphs
#             for sup in p("sup"):  # clears all wikipedia annotations
#                 sup.decompose()
#             description = description + p.text + " "
            
#     this_dict = find_by_key_dicts(article_list[i], article_dict)

#     this_dict["info"] = description




# # description section
# p_before_toc = toc.find_all_previous("p")

# description = ""

# for p in p_before_toc:
#     if not p.text.isspace():  # to avoid taking blank paragraphs
#         for sup in p("sup"):  # clears all wikipedia annotations
#             sup.decompose()
#         description = p.text + " " + description

# article_dict["info"] = description

# print(json.dumps(article_dict, indent = 4))