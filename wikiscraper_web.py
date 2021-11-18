from flask import Flask, request
import json
from flask_cors import CORS
from scraper import Scraper

# Configuration

app = Flask(__name__)
CORS(app)  # allows for cross-origin requests

# Route
@app.route("/", methods=['GET'])
def scraper():
    article, full_text, images, image_format, country_data = get_args(request)

    if article:
        return get_article(article, full_text, images, image_format, country_data)
        try:
            this_scraper = Scraper(article)
        except:
            return "<h1>Sorry that article was not found!<h1>"
        
        if full_text == "y":
            try:
                this_scraper.table_of_content_creator()
                this_scraper.article_text_retriever()
                this_scraper.get_basic_description()
            except:
                return "<h1>Sorry there was an error retrieving the article text<h1>"
        else:
            try:
                this_scraper.get_basic_description()
            except:
                return "<h1>Sorry there was an error retrieving the article text<h1>"
            
        if images == "y":
            try:
                if image_format == 'list':
                    this_scraper.get_images(format="list")
                elif image_format == "dictionary":
                    this_scraper.get_images(format="dictionary")
                else:
                    this_scraper.get_images(format="main")
            except:
                return "<h1>Sorry there was an error retrieving the images, try different parameters.<h1>"
        
        if country_data == "y":
            this_scraper.get_area()
            this_scraper.get_capital()
            this_scraper.get_GDP()
            this_scraper.get_population()
            this_scraper.get_language()
            this_scraper.get_currency()
        
        future_response = json.dumps(this_scraper.article_dict)
        future_response = future_response.replace('\\n', ' ')
        future_response = future_response.replace('\\u00a0', ' ')
        future_response = future_response.replace('\\u2013', '-')
        future_response = future_response.replace('\\u2014', '-')
        future_response = future_response.replace('\\u00f3', 'o')
        future_response = future_response.replace('\\u00fc', 'u')
        future_response = future_response.replace('\\u00e9', 'e')
        future_response = future_response.replace('\\ufeff', '')
        future_response = future_response.replace('\\u00b0', 'degrees')
        
        response = app.response_class(
            response=future_response,
            status=200,
            mimetype='application/json'
        )
        return response
    
    return 'Please enter article in query parameters'

def get_article(article, full_text, images, image_format, country_data):
    try:
        this_scraper = Scraper(article)
    except:
        return "<h1>Sorry that article was not found!<h1>"
    
    if not get_text(this_scraper, full_text):
        return "<h1>Sorry there was an error retrieving the article text<h1>"
    
def get_text(scraper, full_text):
    
    if full_text == 'y':
        try:
            scraper.table_of_content_creator()
            scraper.article_text_retriever()
            scraper.get_basic_description()
        except:
            return False
    else:
        try:
            scraper.get_basic_description()
        except:
            return False
        
    return True
    
    
def get_args(request):
    article = request.args.get("article")
    full_text = request.args.get("full_text")
    images = request.args.get("images")
    image_format = request.args.get("image_format")
    country_data = request.args.get("country_data")
    
    return article, full_text, images, image_format, country_data

# Listener

if __name__ == "__main__":
    app.run(port=6249, debug=True) 