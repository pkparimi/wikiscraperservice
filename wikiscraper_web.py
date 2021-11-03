from flask import Flask, request
import json
from scraper import Scraper

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
        
        return this_scraper.article_dict
    
    return 'Please enter article in query parameters'

# Listener

if __name__ == "__main__":
    app.run(port=6231, debug=True) 