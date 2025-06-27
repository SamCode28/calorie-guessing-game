from flask import Flask, request, jsonify, render_template
from requests_oauthlib import OAuth1Session
import os
import requests

app = Flask(__name__)

#Credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def test_func():
    return render_template("index.html")

@app.route('/get-token')
def get_token():
    token_url = 'https://oauth.fatsecret.com/connect/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope' : 'premiere'
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_info = response.json()
        return jsonify(token_info)
    else:
        return jsonify({'error': 'Failed to get token', 'details': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

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
