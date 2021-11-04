from bs4 import BeautifulSoup
import requests
import locale


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

            if i == 0:
                cur = self.soup.find_all(string=self.article_list[i])[1]
                num_elem = 1
                while cur.parent.parent.name not in ('h1', 'h2', 'h3', 'h4', 'h5'):
                    num_elem += 1
                    cur = self.soup.find_all(string=self.article_list[i])[num_elem]
                cur = cur.parent.parent
            else:
                cur = next_stop
                
            next_stop = self.soup.find_all(string=self.article_list[i+1])[1]
            num_elem = 1
            while next_stop.parent.parent.name not in ('h1', 'h2', 'h3', 'h4', 'h5'):
                num_elem += 1
                next_stop = self.soup.find_all(string=self.article_list[i+1])[num_elem]
            next_stop = next_stop.parent.parent
            
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
            print("-processing " + self.article_list[i])

    def get_basic_description(self):
        toc_soup = self.soup.find(id="toc")
        p_before_toc = toc_soup.find_all_previous("p")
        pre_toc_description = ""

        for p in p_before_toc:
            if not p.text.isspace():  # to avoid taking blank paragraphs
                for sup in p("sup"):  # clears all wikipedia annotations
                    sup.decompose()
                pre_toc_description = p.text + " " + pre_toc_description

        self.article_dict["info"] = pre_toc_description
        
    
    def get_images(self):
        self.article_dict["images"] = {}
        image_dict = self.article_dict["images"]

        images = self.soup.findAll('img')
        for image in images:
            if image.has_attr('alt') and image.has_attr('src') and image['alt'] != '':
                if image['alt'] != 'Page semi-protected':
                    print("-processing image" + image['alt'])
                    image_dict[image['alt']] = image['src']
            
    def get_capital(self):
        try:
            capital = self.soup.find('th',text="Capital")
            capitalname = capital.next_sibling.text
            capital_name_breakpoint = None
            capital_gps_breakpoint = None
            for i in range(len(capitalname)):
                if not capital_name_breakpoint and capitalname[i].isdigit():
                    capital_name_breakpoint = i
                if not capital_gps_breakpoint and capitalname[i] == '\ufeff':
                    capital_gps_breakpoint = i

            self.article_dict["capital_name"] = capitalname[:capital_name_breakpoint]
            self.article_dict["capital_gps"] = capitalname[capital_name_breakpoint:capital_gps_breakpoint]    
        except:
            self.article_dict["capital_name"] = "NOT FOUND IN THIS ARTICLE"
            self.article_dict["capital_gps"] = "NOT FOUND IN THIS ARTICLE"
    def get_language(self):
        try:
            official_languages = self.soup.find(name='th', text='Official\xa0languages')
            self.article_dict["language_name"] = official_languages.next_sibling.find('a').text
        except:
            self.article_dict["language_name"] = "NOT FOUND IN THIS ARTICLE"
            
    def get_population(self):
        try:
            population = self.soup.find('a', text='Population').parent.parent.nextSibling.find(class_='infobox-data').text
            population = population.strip()
            for i in range(len(population)):
                if not population[i].isdigit() and population[i] != ',':
                    self.article_dict["population"] = population[:i]
                    break
        except:
            self.article_dict["population"] = "NOT FOUND IN THIS ARTICLE"
    
    def get_GDP(self):
        try:
            GDP_total = self.soup.find('a', text='GDP').parent.parent.nextSibling.find(class_='infobox-data').text
            GDP_total = GDP_total.strip()
            for i in range(len(GDP_total)):
                if GDP_total[i] ==  'n':
                    self.article_dict["GDP_total"] = GDP_total[:i+1]
                    break
        except:
            self.article_dict["GDP_total"] = "NOT FOUND IN THIS ARTICLE"
        
        try:    
            GDP_per_cap = self.soup.find('a', text='GDP').parent.parent.nextSibling.nextSibling.find(class_='infobox-data').text
            GDP_per_cap = GDP_per_cap.strip()
            for i in range(len(GDP_per_cap)):
                if not GDP_per_cap[i].isdigit() and GDP_per_cap[i] != ',' and GDP_per_cap[i] != '$':
                    self.article_dict["GDP_per_cap"] = GDP_per_cap[:i]
                    break
        except:
            self.article_dict["GDP_per_cap"] = "NOT FOUND IN THIS ARTICLE"
            
    def get_area(self):
        try:
            area = self.soup.find('a', text='Area ').parent.parent.nextSibling.find(class_='infobox-data').text
            area = area.strip()
            locale.setlocale(locale.LC_ALL, 'en_US')
            for i in range(len(area)):
                if area[i] == '\xa0':
                    self.article_dict["area_km"] = area[:i] + " km^2"
                    self.article_dict["area_mi"] = locale.format("%d", int(int(area[:i].replace(",","")) * 0.386102), grouping=True) + " mi^2"
                    break
        except:
            self.article_dict["area_km"] = "NOT FOUND IN THIS ARTICLE"
            self.article_dict["area_mi"] = "NOT FOUND IN THIS ARTICLE"
        
        
if __name__ == "__main__":
    this_scraper = Scraper("United_States")
    
    this_scraper.table_of_content_creator()
        
    this_scraper.article_text_retriever()
    
    print(this_scraper.article_dict)