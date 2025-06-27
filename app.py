from flask import Flask, request, jsonify, render_template
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
        print("Found token")
        print(token_found.get("access_token"))
    else:
        return jsonify({'error': 'Failed to get token', 'details': response.text}), response.status_code
    
@app.route('/get-food', methods=['POST'])
def get_food():
    print(token_found.get("access_token"))
    token_url = 'https://platform.fatsecret.com/rest/server.api'
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : f"Bearer {token_found.get("access_token")}"
    }
    payload = {
        'method' : 'food.search',
        'search_expression' : "toast",
        'format' : "json"
    }

    response = requests.post(token_url, headers=headers, json=payload)

    if response.status_code == 200:
        data_found = response.json()
        return jsonify(data_found)
    else:
        print('Error:', response.status_code, response.text)
        return None


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
