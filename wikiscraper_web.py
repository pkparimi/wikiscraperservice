from flask import Flask, request
from json import dumps
from flask_cors import CORS
from scraper import Scraper

# Configuration

app = Flask(__name__)
CORS(app)  # allows for cross-origin requests

# Route
@app.route("/", methods=['GET'])
def scraper():
    """
    get:
        summary: Scrapes the wikipedia areticle and serves a JSON via a get request.
        parameters:
            -article: article name of wikipedia article
            -full_text: y if full text is wanted, n if only description, default is n
            -images: y if images are requires, n if not, default is n
            -image_format: dict for dictionary, list for list, main for just main images, default is main
        responses:
            200:
                if article parameters are valid:
                    content: application/json 
                else:
                    html text of error
    """
    
    # get arguments
    article, full_text, images, image_format, country_data = get_args(request)

    # proceeds through scraping cascade if article param is given
    if article:
        this_scraper = get_article(article)
        if not this_scraper:  # if scraper object returns error when searching for article
            return "<h1>Sorry that article was not found!<h1>"
        
        this_scraper = get_text(this_scraper, full_text)
        if not this_scraper:  # if scraper object returns error when searching for article text
            return "<h1>Sorry there was an error retrieving the article text<h1>"

        this_scraper = get_images(this_scraper, image_format, images)
        if not this_scraper:  # if scraper object returns error when searching for article images
            return "<h1>Sorry there was an error retrieving the images, try different parameters.<h1>"
        
        this_scraper = get_country_data(this_scraper, country_data)
        if not this_scraper:  # if scraper object returns error when searching for article country data
            return "<h1>Sorry there was an error retrieving the country data, try different parameters.<h1>"
        
        # format response
        response = app.response_class(
            response=replace_strange_chars(dumps(this_scraper.article_dict)),
            status=200,
            mimetype='application/json'
        )
        return response
    
    # if no article given in params
    return 'Please enter article in query parameters'

def replace_strange_chars(str_to_replace: str) -> str:
    """
    Replaces misparsed UTF characters with equivalents.
    """
    
    replacements = {'\\n':' ', 
                    '\\u00a0' : ' ',
                    '\\u2013' : '-',
                    '\\u2014' : '-',
                    '\\u00f3' : 'o',
                    '\\u00fc' : 'u',
                    '\\u00e9' : 'e',
                    '\\ufeff' : '',
                    '\\u00b0' : 'degrees'
                }
    
    for key, value in replacements.items():
        str_to_replace = str_to_replace.replace(key, value)

    return str_to_replace
    
def get_country_data(this_scraper: object, country_data: str) -> object:
    """
    Performs country data scrape for current scraper.
    """
    
    if country_data == "y":
        try:
            this_scraper.get_area()
            this_scraper.get_capital()
            this_scraper.get_GDP()
            this_scraper.get_population()
            this_scraper.get_language()
            this_scraper.get_currency()
        except:
            return None
        
    return this_scraper
            
        

def get_article(article: str) -> object:
    """
    Creates article scraper object given article title text.
    """
    
    try:
        this_scraper = Scraper(article)
    except:
        return None
    
    return this_scraper
    
def get_text(this_scraper: object, full_text: str) -> object:
    """
    Performs text scrape for current scraper.
    """
    
    if full_text == 'y':
        try:
            this_scraper.table_of_content_creator()
            this_scraper.article_text_retriever()
            this_scraper.get_basic_description()
        except:
            return None
    else:
        try:
            this_scraper.get_basic_description()
        except:
            return None
        
    return this_scraper

def get_images(this_scraper: object, image_format: str, images: str) -> object:
    """
    Performs image scrape for current scraper.
    """
    
    if images == "y":
        try:
            if image_format == 'list':
                this_scraper.get_images(format="list")
            elif image_format == "dictionary":
                this_scraper.get_images(format="dictionary")
            else:
                this_scraper.get_images(format="main")
        except:
            return None
        
    return this_scraper
     
def get_args(request: object) -> tuple:
    """
    Retrieves arguments from get request.
    """
    
    article = request.args.get("article")
    full_text = request.args.get("full_text")
    images = request.args.get("images")
    image_format = request.args.get("image_format")
    country_data = request.args.get("country_data")
    
    return article, full_text, images, image_format, country_data

# Listener

if __name__ == "__main__":
    app.run(port=6249, debug=True) 