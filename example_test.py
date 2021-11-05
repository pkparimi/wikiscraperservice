import requests
import json

country_URL = "http://flip3.engr.oregonstate.edu:6231/?article=China&full_text=n"
country_URL_with_country_data = "http://flip3.engr.oregonstate.edu:6231/?article=China&full_text=n&country_data=y"
country_URL_with_full_text = "http://flip3.engr.oregonstate.edu:6231/?article=China&full_text=y"
country_URL_with_images_dict = "http://flip3.engr.oregonstate.edu:6231/?article=China&full_text=n&images=y&image_format=dictionary"
country_URL_with_images_list = "http://flip3.engr.oregonstate.edu:6231/?article=China&full_text=n&images=y&image_format=list"
country_URL_with_images_main = "http://flip3.engr.oregonstate.edu:6231/?article=China&full_text=n&images=y&image_format=main"
country_URL_with_all = "http://flip3.engr.oregonstate.edu:6231/?article=China&full_text=y&country_data=y&images=y"

animal_URL = "http://flip3.engr.oregonstate.edu:6231/?article=Elephant&full_text=n"
animal_URL_with_country_data = "http://flip3.engr.oregonstate.edu:6231/?article=Elephant&country_data=y"
animal_URL_with_images_dict = "http://flip3.engr.oregonstate.edu:6231/?article=Elephant&images=y&image_format=dictionary"
animal_URL_with_images_list = "http://flip3.engr.oregonstate.edu:6231/?article=Elephant&images=y&image_format=list"
animal_URL_with_images_main = "http://flip3.engr.oregonstate.edu:6231/?article=Elephant&images=y&image_format=main"
animal_URL_with_full_text = "http://flip3.engr.oregonstate.edu:6231/?article=Elephant&full_text=y"
animal_URL_with_all_except_country = "http://flip3.engr.oregonstate.edu:6231/?article=Elephant&full_text=y&images=y"

def example_chooser():
    while True:
        an_or_co = input("Do you want to: \n A) show an example of a country URL \n or \n B) show an example of an animal URL \n")
        if an_or_co in ['A', 'B']:
            break
    while True:
        which_example = input("Do you want to: \n A) show an example with just a description \n B) show an example with country data  \n C) show an example with full text \n D) show an example with images in dict \n E) show an example with images in list \n F) show an example with only main images \n G) show an example with all parameters \n")
        if which_example in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            break
    if an_or_co == 'A':
        if which_example == 'A':
            URL = country_URL
        elif which_example == 'B':
            URL = country_URL_with_country_data
        elif which_example == 'C':
            URL = country_URL_with_full_text
        elif which_example == 'D':
            URL = country_URL_with_images_dict
        elif which_example == 'E':
            URL = country_URL_with_images_list
        elif which_example == 'F':
            URL = country_URL_with_images_main
        elif which_example == 'G':
            URL = country_URL_with_all
    elif an_or_co == 'B':
        if which_example == 'A':
            URL = animal_URL
        elif which_example == 'B':
            URL = animal_URL_with_country_data
        elif which_example == 'C':
            URL = animal_URL_with_full_text
        elif which_example == 'D':
            URL = animal_URL_with_images_dict
        elif which_example == 'E':
            URL = animal_URL_with_images_list
        elif which_example == 'F':
            URL = animal_URL_with_images_main
        elif which_example == 'G':
            URL = animal_URL_with_all_except_country 
              
    r = requests.get(url=URL)
    
    new_dict = json.loads(r.content)
    print("done")
    
    
if __name__ == '__main__':
    example_chooser()