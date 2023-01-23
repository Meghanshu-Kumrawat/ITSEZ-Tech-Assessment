# Question 2: Find out you total expense on swiggy and store the details in database.
# Details: 1. Total expense.
#               2. Expense in last 4 months
#               3. Most ordered Dish, most favorite restaurant, Avg order value. (store in sql database)

import requests
import sqlite3
import collections

def scrap_orders():
    '''
    function to scrape the orders
    '''
    ORDER_URL = "https://www.swiggy.com/dapi/order/all?order_id="

    headers = {
        "authority": "www.swiggy.com",
        "__fetch_req__": "true",
        "accept-language": "en-US,en;q=0.9,hi;q=0.8",
        "content-type": "application/json",
        "cookie": "__SW=oO2YBVGqmH1PwOFH4HPQGTDPsqwad55t; _device_id=c988b34f-d58e-e99e-a9c6-124ada742588; fontsLoaded=1; _gcl_au=1.1.1830066694.1673635481; _gid=GA1.2.503476897.1674482537; swgy_logout_clear=1; _sid=4zvb5702-e360-4a3d-b7f2-3be46924365a; _is_logged_in=1; _session_tid=e4625a5260817b06c0c431cb1afa57598350a21a496727b1f3c406142d3386889d274be298c5580a1a06e039f6ffdcafb782861a2ba8de6fb39ae63441cd3e03f1ef74b8a519d22c3c673d69a13aaea6624dec3437d7e3a57416172cd4fe904d745b56d7b2eee8352f498bdd6fec1345; _gat_UA-53591212-4=1; userLocation=^%^7B^%^22lat^%^22^%^3A^%^2222.693376^%^22^%^2C^%^22lng^%^22^%^3A^%^2275.88019^%^22^%^2C^%^22address^%^22^%^3A^%^22Kaushalyapuri^%^2C^%^20Indore^%^2C^%^20Madhya^%^20Pradesh^%^20452001^%^2C^%^20India^%^22^%^2C^%^22area^%^22^%^3A^%^22Kaushalyapuri^%^22^%^2C^%^22id^%^22^%^3A^%^22160287801^%^22^%^7D; adl=true; _gat_0=1; _ga_34JYJ0BCRN=GS1.1.1674482537.9.1.1674482648.0.0.0; _ga=GA1.1.447013592.1673635481; WZRK_G=921cab885ae9443eb35c2aaa707f697e; WZRK_S_W86-ZZK-WR6Z=^%^7B^%^22s^%^22^%^3A1674482537^%^2C^%^22t^%^22^%^3A1674482648^%^7D",
        "if-none-match": "W/^\\^\"1eb49-2fbbIgDknYwcMab5H2NdqEKMcq4^\\^\"",
        "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    resp = requests.get(ORDER_URL, headers=headers).json()

    data = []
    for order in resp['data']['orders']:
        detail = {}
        detail['price'] = order['payment_transactions'][0]['amount']
        detail['item'] = order['order_items'][0]['name']
        detail['restaurant'] = order['restaurant_name']
        detail['order_time'] = order['order_time']
        data.append(detail)

    return data


def sql_db_store(data):
    '''
    function to store data in SQL database
    '''
    connection = sqlite3.connect("swiggydb.db")
    cursor = connection.cursor()
    
    create_table = """CREATE TABLE IF NOT EXISTS swiggy (id INTEGER NOT NULL PRIMARY KEY, order_time VARCHAR(100), item VARCHAR(100), restaurant VARCHAR(100), price INTEGER);"""
    cursor.execute(create_table)

    for id, row in enumerate(data):
        insert_data = f"""INSERT INTO swiggy VALUES ({id}, "{row['order_time']}", "{row['item']}", "{row['restaurant']}", {row['price']});"""
        cursor.execute(insert_data)
        connection.commit()

    total_expense = """SELECT SUM(price) FROM swiggy;"""
    cursor.execute(total_expense)
    value = cursor.fetchall()[0][0]
    print("Total expense :", value)   
    print("Avg order value :", value/len(data))   

    max_order = collections.Counter(e['item'] for e in data)
    print("Most ordered Dish :", max(max_order.keys(), key=lambda x:x[1]))   
    
    max_rest = collections.Counter(e['restaurant'] for e in data)
    print("Most favorite restaurant :", max(max_rest.keys(), key=lambda x:x[1]))   

    connection.close()


if __name__=="__main__":
    data = scrap_orders()
    print(data)
    sql_db_store(data)