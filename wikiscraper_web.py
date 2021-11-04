from flask import Flask, request
import json
from scraper import Scraper
import unicodedata

# Configuration

app = Flask(__name__)

# Routes
@app.route("/", methods=['GET'])
def scraper():
    article = request.args.get("article")
    if article:
        this_scraper = Scraper(article)
        
        this_scraper.table_of_content_creator()
        
        this_scraper.article_text_retriever()
        
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