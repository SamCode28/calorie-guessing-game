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
        #required
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token_found.get("access_token")}"
    }
    params = {
        #required
        'method' : 'foods.search.v3',
        'format' : "json",
        #optional
        'region' : 'US',
        'page_number' : 0,
        'max_results' : 5,
        'search_expression' : f'"{return_random_whole_food()}"', #Placeholder
        'include_food_images' : True,        
    }

    response = requests.get(token_url, headers=headers, params=params)
    response = response.json()

    food_list = response['foods_search']['results']['food']

    try:
        valid_food = return_valid_food_from_list(food_list)
    except KeyError:
        pass
        #Create error to retry with new search term

    #Object to be sent back
    food_data = {'food_name' : valid_food['food_name'],
                 'img_url' : valid_food['food_images']['food_image'][0]['image_url'],
                 'protein' : "",
                 'carbs' : "",
                 'fiber' : "",
                 'fat' : "",
                 'calories' : ""
                 }

    #Check to see if food contains data with 100g serving size
    for serving in valid_food['servings']['serving']:
        if serving['serving_description'] == "100 g":
            food_data['protein'] = f'{serving['protein']} g'
            food_data['carbs'] =  f'{serving['carbohydrate']} g'
            food_data['fiber'] =  f'{serving['fiber']} g'
            food_data['fat'] = f'{serving['fat']} g'
            food_data['calories'] = f'{serving['calories']} kcal'
            #print(f"food:{food_data}")
            return jsonify(food_data)
    print("No match found")
        #Create error if none found
            
    #saved for future use
    #except KeyError:
    #    return jsonify({'error': 'Invalid JSON from FatSecret', 'raw': response.text}), 502
    

def return_valid_food_from_list(food_dict):
    num_results = len(food_dict)
    random_key = random.randint(0, num_results - 1)
    test_key = random_key + 1

    while(random_key != test_key):
        if (test_key == num_results):
                test_key = 0
        if('food_images' in food_dict[test_key] and food_dict[test_key]['food_type'] == "Generic"):
            print(f"Found: {food_dict[test_key]['food_name']}")
            return food_dict[test_key]
        print(f"Not found: {food_dict[test_key]['food_name']}")
        test_key += 1
    
    return KeyError


whole_food_list = ['apple', 'avocados', 'banana', 'blueberry', 'cherry', 'grape', 'grapefruit', 'kiwi', 'lemon', 'lime', 
 'mandarin', 'mango', 'melon', 'orange', 'peach', 'pear', 'pineapple', 'pomegranate', 'strawberry', 'watermelon',
 'arugula', 'asparagus', 'bell pepper', 'bok choy', 'broccoli', 'brussels sprout', 'cabbage', 'carrot', 
 'cauliflower', 'celery', 'corn', 'cucumber', 'eggplant', 'green bean', 'kale', 'leek', 'lettuce', 
 'mushroom', 'pea', 'potato', 'radish', 'red onion', 'spinach', 'sweet potato', 'tomato', 'turnip', 'yellow squash', 
 'zucchini','almond', 'brazil nut', 'cashew', 'chestnut', 'hazelnut', 'macadamia', 'peanut', 'pecan', 'pine nut', 'pistachio', 'walnut',
 'chia seed', 'flaxseed', 'hemp seed', 'pumpkin seed', 'sesame seed', 'sunflower seeds',]

food_num = -1

def return_random_whole_food():
    global food_num
    food_num += 1
    return whole_food_list[food_num]
    

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)


#curl -X 'GET' \
#  'https://api.nal.usda.gov/fdc/v1/food/2262074?format=abridged&nutrients=957&nutrients=203&nutrients=204&nutrients=205' \
#  -H 'accept: application/json'

#{
#  "foods_search": {
#    "max_results": "20",
#    "total_results": "2004",
#    "page_number": "0",
#    "results": {
#      "food": [
#        {
#          "food_id": "35718",
#          "food_name": "Apples",
#          "food_type": "Generic",
#          "food_url": "https://foods.fatsecret.com/calories-nutrition/usda/apples",
#          "food_images": {
#            "food_image": [
#              {
#                "image_url": "https://www.foodimagedb.com/food-images/6b5d0828-7391-49e6-ba02-606b0363d41e_1024x1024.png",
#                "image_type": "0"
#              },
#              {
#                "image_url": "https://www.foodimagedb.com/food-images/6b5d0828-7391-49e6-ba02-606b0363d41e_400x400.png",
#                "image_type": "0"
#              },
#              {
#                "image_url": "https://www.foodimagedb.com/food-images/6b5d0828-7391-49e6-ba02-606b0363d41e_72x72.png",
#                "image_type": "0"
#              }
#            ]
#          },
#          "servings": {
#            "serving": [
#              {
#                "serving_id": "32915",
#                "serving_description": "1 medium (2-3/4\" dia) (approx 3 per lb)",
#                "serving_url": "https://foods.fatsecret.com/calories-nutrition/usda/apples?portionid=32915&portionamount=1.000",
#                "metric_serving_amount": "138.000",
#                "metric_serving_unit": "g",
#                "number_of_units": "1.000",
#                "measurement_description": "medium (2-3/4\" dia) (approx 3 per lb)",
#                "is_default": "1",
#                "calories": "72",
#                "carbohydrate": "19.06",
#                "protein": "0.36",
#                "fat": "0.23",
#                "saturated_fat": "0.039",
#                "polyunsaturated_fat": "0.070",
#                "monounsaturated_fat": "0.010",
#                "cholesterol": "0",
#                "sodium": "1",
#                "potassium": "148",
#                "fiber": "3.3",
#                "sugar": "14.34",
#                "vitamin_a": "4",
#                "vitamin_c": "6.3",
#                "calcium": "8",
#                "iron": "0.17"
#              },
             