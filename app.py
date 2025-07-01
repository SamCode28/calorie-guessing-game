from flask import Flask, request, jsonify, render_template, Response
import os
import requests
import random
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
    
@app.route('/get-food', methods=['GET'])
def get_food():
    token_url = 'https://platform.fatsecret.com/rest/foods/search/v3'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token_found.get("access_token")}"
    }
    payload = {
        'method' : 'foods.search.v3',
        'search_expression' : "apple",
        'format' : "json"

    }

    response = requests.get(token_url, headers=headers, params=payload)
    response = response.json()

    random_valid_food_dict_key = random.randint(0,len(response['foods_search']['results']['food']))


    try:
        return (f"Food ID for #{random_valid_food_dict_key}: {response['foods_search']['results']['food'][random_valid_food_dict_key]['food_id']}")
    except ValueError:
        return jsonify({'error': 'Invalid JSON from FatSecret', 'raw': response.text}), 502
    



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
