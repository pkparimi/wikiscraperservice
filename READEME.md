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
