def find_by_key(value, dic):
    # iterates through nested dictionary to find key 
    if value in dic:
        return dic[value]
    for v in dic.values():
        if isinstance(v, dict):
            if v != {}:
                return find_by_key(value, v)
    return None

def table_of_content_creator(toc_soup):
    # creates dictionary to store Table of contents
    article_dict = {}
    breaker = False
    level = 1
    section = 1
    level_stack = []  # stack to traverse nested keys
    cur_dict = article_dict

    while not breaker:
        cur_bullet = toc_soup.select('li[class*="tocsection-' + str(section) + '"]')[0]  # gets current TOC list item tag object
        section_text = cur_bullet.select(".toctext")[0].text # gets text of TOC list item
        
        if section_text in ("See also", "See Also", "Notes", "References"):
            break
        
        cur_level = int(cur_bullet['class'][0][9])

        if cur_level == level:
            if not level_stack:
                article_dict[section_text] = {}
                cur_dict = article_dict
                level_stack.append(section_text)
            else:
                level_stack.pop()
                cur_dict[section_text] = {}
                level_stack.append(section_text)
        elif cur_level > level:
            level = cur_level
            cur_dict = cur_dict[level_stack[-1]]
            cur_dict[section_text] = {}
            level_stack.append(section_text)
        elif cur_level < level:
            num_to_pop = level - cur_level + 1
            level = cur_level
            for i in range(num_to_pop):
                if level_stack:
                    level_stack.pop()
            if not level_stack:
                article_dict[section_text] = {}
                cur_dict = article_dict
                level_stack.append(section_text)
            else:
                cur_dict = find_by_key(level_stack.pop(), article_dict)
                cur_dict[section_text] = {}
                level_stack.append(section_text)
                
        section += 1
    return article_dict