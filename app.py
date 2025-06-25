from flask import Flask, request, jsonify
from requests_oauthlib import OAuth1Session

app = Flask(__name__)

# Replace with your FatSecret credentials
consumer_key = 'your_key'
consumer_secret = 'your_secret'

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
    app.run(debug=True)