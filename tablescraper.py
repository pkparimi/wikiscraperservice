from MySQLdb import STRING
from bs4 import BeautifulSoup
import requests
import locale

URL = "https://en.wikipedia.org/wiki/India"

resp = requests.get(URL)
        
soup = BeautifulSoup(resp.text, 'html.parser')

# def capital:
#     capital = soup.find('th',text="Capital")
#     capitalname = capital.next_sibling.text
#     capital_name_breakpoint = None
#     capital_gps_breakpoint = None
#     for i in range(len(capitalname)):
#         cur_char = capitalname[i]
#         if not capital_name_breakpoint and capitalname[i].isdigit():
#             capital_name_breakpoint = i
#         if not capital_gps_breakpoint and capitalname[i] == '\ufeff':
#             capital_gps_breakpoint = i

#     capital_name = capitalname[:capital_name_breakpoint]
#     capital_gps = capitalname[capital_name_breakpoint:capital_gps_breakpoint]

# def languages:
#     offcial_languages = soup.find(name='th', text='Official\xa0languages')
#     language_name = offcial_languages.next_sibling.find('a').text

# def population:
#     population = soup.find('a', text='Population').parent.parent.nextSibling.find(class_='infobox-data').text
#     population = population.strip()
#     for i in range(len(population)):
#         if not population[i].isdigit() and population[i] != ',':
#             population = population[:i]
#             break

#     print(population[:pop_end_char])
# def GDP:
#     GDP_total = soup.find('a', text='GDP').parent.parent.nextSibling.find(class_='infobox-data').text
#     GDP_total = GDP_total.strip()
#     for i in range(len(GDP_total)):
#         if GDP_total[i] ==  'n':
#             GDP_total = GDP_total[:i+1]
#             break
#     print(GDP_total)

#     GDP_per_cap = soup.find('a', text='GDP').parent.parent.nextSibling.nextSibling.find(class_='infobox-data').text
#     GDP_per_cap = GDP_per_cap.strip()
#     for i in range(len(GDP_per_cap)):
#         if not GDP_per_cap[i].isdigit() and GDP_per_cap[i] != ',' and GDP_per_cap[i] != '$':
#             GDP_per_cap = GDP_per_cap[:i]
#             break
#     print(GDP_per_cap)

# def Area:
    # area = soup.find('a', text='Area ').parent.parent.nextSibling.find(class_='infobox-data').text
    # area = area.strip()
    # locale.setlocale(locale.LC_ALL, 'en_US')
    # for i in range(len(area)):
    #     if area[i] == '\xa0':
    #         area_km = area[:i] + " km^2"
    #         area_mi = locale.format("%d", int(int(area[:i].replace(",","")) * 0.386102), grouping=True) + " mi^2"
    #         break
    # print(area_km, area_mi)
    
currency = soup.find('th', text='Currency').nextSibling.text

print(currency)