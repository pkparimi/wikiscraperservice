from flask import Flask, request
import json
from scraper import Scraper

# Configuration

app = Flask(__name__)

# Routes
@app.route("/", methods=['GET'])
def scraper():
    article = request.args.get("article")
    full_text = request.args.get("full_text")
    images = request.args.get("images")
    image_format = request.args.get("image_format")
    country_data = request.args.get("country_data")
    print(full_text)
    if article:
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

# Listener

if __name__ == "__main__":
    app.run(port=6231, debug=True) 