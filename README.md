# Wikipedia Web Scraper

Wikipedia Web Scraper is a microservice for scraping data from a specific webpage

## Overview

This guide will provide an overview of the Following:
- What this web app does
- Setup of the wiki scraper locally
- Using the wiki scraper remotely through OSU VPN

## What does this web app do?
This web app receives HTTP GET requests with specific parameters (article, full_text, images, image_format, country data) and returns a JSON formatted web scrape of the wikipedia article determined by the article parameter. 

## Setup Locally (Note: Not needed for CS361 teammates)
### Requirements
#### Install Flask and its Dependencies

Recommend to do this in a virtual environment

```bash
pip3 install flask-mysqldb
```

#### Install BeautifulSoup

Recommend to do this in a virtual environment

```bash
pip3 install beautifulsoup4
```

#### Change to desired port on wikiscraper_web.py
```python
if __name__ == "__main__":
    app.run(port=6232)
```

#### Run wikiscraper_web.py
```bash
python3 wikiscraper_web.py
```

This will start a temporary instance on the port specified (ctrl+C or exiting your IDE/terminal will kill this) 

#### To run this persistently
We need to install gunicorn

```bash
pip3 install gunicorn
```

Once installed we need a file for Gunicorn to use and know what app to serve. Create a file called `wsgi.py`. We just need a few lines of code.

```python
from wikiscraper_web import app

if __name__ == "__main__":
    app.run()
```
Lastly, we go back to our terminal and run `gunicorn`.

```bash
# 0.0.0.0 here can be whatever address your server is hosted
gunicorn --bind 0.0.0.0:<your-desired-port-here> wsgi:app -D
```

 `-D` switch is important here. This switch tells Gunicorn to 'daeomonize' its process, which allows it to run in the background, and will not exit when you logoff, close your terminal or exit your IDE. If you are testing and *DO NOT want the application to stay alive after logging off* omit the `-D` switch.

Once Gunicorn is running, you should be able to navigate to `localhost:port` on your browser where `port` is the port you specified when you ran Gunicorn and see your webapp in all of its glory!

If you run Gunicorn with the `-D` switch, you'll likely wonder, well how do I close it. Open your terminal

```bash
ps ax | grep gunicorn
```

You will see 4 or 5 digit integers on the left, the very first number is the number of the main `gunicorn` process we want to `kill`.

Once you `kill` the process will shut down and the web server is no longer running. You can restart it again however you would like.

## Using the wiki scraper remotely through OSU VPN
None of the files here are needed use this app locally. If you are connected via the OSU VPN if will be hosted on flip3 port 6231: 

http://flip3.engr.oregonstate.edu:6231/

### Parameters:
The following parameters allow for a variety of returns within the JSON file. 
* article
     * This is required at a minimum, the title of the wiki article to scrape.
     * http://flip3.engr.oregonstate.edu:6231/?article=*yourarticlehere*
* full_text
     * if this is 'y': entire table of contents with text for each section will be provided in the return JSON - nested by the table of contents
     * This will take some time so if the brief description is all you need 'n' is recommended here
     * defaulted to 'n' (no) which will provide only the article text before the table of contents
     * http://flip3.engr.oregonstate.edu:6231/?article=*yourarticlehere*&full_text=*y*
* country_data
     * if this is 'y': return JSON will have the below easily retrievable keys and values (values are all string formatted)
          * capital_name - name of capital city
          * capital_gps - gps coordinates of capital city
          * language_name - official language(s)
          * population - population of country
          * GDP_total - PPP total GDP of country (string formatted)
          * GDP_per_cap - PPP GDP per capita of country (string formatted)
          * area_km - area of country in km squared  
          * area_mi - area of country in mi squared
          * currency - currency of country
     * If 'y' is entered as a parameter but no country data exists (i.e. for an animal) each of these keys' values will be "NOT FOUND IN THIS ARTICLE"
     * defaulted to 'n' (no) which will not provide any quick country info
     * http://flip3.engr.oregonstate.edu:6231/?article=*yourarticlehere*&country_data=*y*
* images
     * if this is 'y': return JSON will include links to images the article as a list/dict as a value of the 'images' key 
     * image_format parameter is defaulted to 'main' so only the main images of the article will return
* image_format
     * if this is 'dictionary': return JSON will include links to ALL OF THE images the article as a dictionary as a value of the 'images' key
          * This may take a lot of time so not recommended
     * if this is 'list': return JSON will include links to ALL OF THE images the article as a listas a value of the 'images' key
          * This may take a lot of time so not recommended
     * if this is 'main': return JSON will include links to ONLY THE MAIN images (i.e sidebar images) of the article as a list as a value of the 'images' key
          * This is relatively quick so if you need to pull a country flag or animal image this is recommended
          * country flag or animal image will likely be 1st image in list so:
               * returnJSONasDict["images"][0] will likely be a flag for a country

### example_test.py:
I recommend running this file and inputting a breakpoint on line 62 with a watch on new_dict to see the format of the JSON/dict for each option listed.
