from flask import Flask, request, jsonify, render_template, Response
import os
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

#Credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

token_found = None

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/get-token', methods=['POST'])
def get_token():
    global token_found
    token_url = 'https://oauth.fatsecret.com/connect/token'
    data = {
        'grant_type': 'client_credentials',
        'scope' : 'premier'
    }

    response = requests.post(
        token_url,
        data=data,
        auth=HTTPBasicAuth(client_id, client_secret)
    )

    if response.status_code == 200:
        token_found = response.json()
        return Response(status=204)
    else:
        return jsonify({'error': 'Failed to get token', 'details': response.text}), response.status_code
    
@app.route('/get-food', methods=['POST'])
def get_food():
    token_url = "https://platform.fatsecret.com/rest/server.api"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token_found.get("access_token")}"
    }
    payload = {
        'method' : 'foods.search',
        'search_expression' : "apple",
        'format' : "json"
    }

    response = requests.post(token_url, headers=headers, json=payload)

    try:
        return jsonify(response.json(), response.status_code)
    except ValueError:
        return jsonify({'error': 'Invalid JSON from FatSecret', 'raw': response.text}), 502


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
