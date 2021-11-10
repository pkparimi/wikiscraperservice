from wikiscraper_web import app

if __name__ == '__main__':
    app.run()

# gunicorn --bind 0.0.0.0:<your-desired-port-here> wsgi:app -D