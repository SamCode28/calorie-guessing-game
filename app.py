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
    #Find and store token
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
        #Load HTML, CSS, JS
        return render_template("index.html")
    
    else:
        return f'Error: Failed to get token. Status Code: {response.status_code}' 
            
    
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
        'include_food_images' : True,
        'flag_default_serving' : True,
        'format' : "json"
    }

    response = requests.get(token_url, headers=headers, params=payload)
    response = response.json()

    random_valid_food_dict_key = random.randint(0,len(response['foods_search']['results']['food']))

    print(f'key: {random_valid_food_dict_key}')

    attempts = len(response['foods_search']['results']['food'])

    while(attempts > 1):
        random_valid_food_dict_key = random.randint(0,len(response['foods_search']['results']['food']) - 1)
        try:
            if(response['foods_search']['results']['food'][random_valid_food_dict_key]['food_images']):
                print('Link found')
                print(f'Calories: {response['foods_search']['results']['food'][random_valid_food_dict_key]['servings']['serving'][0]['calories']}')
                break
        except KeyError:
            print('No link found')
            print(f"except #: {random_valid_food_dict_key}")
            attempts -= 1

    try:
        return response['foods_search']['results']['food'][random_valid_food_dict_key]['food_images']['food_image'][0]['image_url']
    except KeyError:
        return jsonify({'error': 'Invalid JSON from FatSecret', 'raw': response.text}), 502
    

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)


#curl -X 'GET' \
#  'https://api.nal.usda.gov/fdc/v1/food/2262074?format=abridged&nutrients=957&nutrients=203&nutrients=204&nutrients=205' \
#  -H 'accept: application/json'