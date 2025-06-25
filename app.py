from flask import Flask, request, jsonify, render_template
from requests_oauthlib import OAuth1Session
import os

app = Flask(__name__)

# Replace with your FatSecret credentials
consumer_key = 'your_key'
consumer_secret = 'your_secret'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return "About page"

@app.route('/api/search-food')
def search_food():
    query = request.args.get('query', '')
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    url = 'https://platform.fatsecret.com/rest/server.api'
    params = {
        'method': 'foods.search',
        'format': 'json',
        'search_expression': query
    }

    resp = oauth.get(url, params=params)
    return jsonify(resp.json())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
