# Question 1: Scrape the API from swiggy + find the cheapest items list in your area + the restaurant and item details.
# Restaurant details: Name, Area, Timing, Distance, Discount, Delivery Fee, Rating
# Item Details: Name, Price, Rating (if available)

import requests

URL = "https://www.swiggy.com/dapi/restaurants/list/v5?lat=22.691778&lng=75.846352&sortBy=COST_FOR_TWO&page_type=DESKTOP_WEB_LISTING"

response = requests.get(URL).json()

data = []
for restaurant in response['data']['cards'][0]['data']['data']['cards']:
    MENU_URL = f"https://www.swiggy.com/dapi/menu/v4/full?menuId={restaurant['data']['id']}"
    menu_response = requests.get(MENU_URL).json()
    
    dish_data = sorted(list(menu_response['data']['menu']['items'].items()), key=lambda k:k[1]['price'])
    
    detail = {}
    detail['name'] = restaurant['data']['name']
    detail['area'] = restaurant['data']['area']
    detail['distance'] = restaurant['data']['lastMileTravelString']
    detail['discount'] = restaurant['data']['aggregatedDiscountInfoV2']['header']
    detail['rating'] = restaurant['data']['avgRating']
    detail['menu'] = {}
    detail['menu']['name'] = dish_data[0][1]['name']
    detail['menu']['price'] = int(str(dish_data[0][1]['price'])[:-1])
    data.append(detail)
    
output = sorted(data, key=lambda k:k['menu']['price'])

print("Restaurant & Item details :", output[0])