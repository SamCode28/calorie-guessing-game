from flask import Flask, request, jsonify, render_template
import os
import requests
from requests.auth import HTTPBasicAuth

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

@app.route('/get-token', methods=['POST'])
def get_token():
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
        token_info = response.json()
        return jsonify(token_info)
    else:
        return jsonify({'error': 'Failed to get token', 'details': response.text}), response.status_code

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
