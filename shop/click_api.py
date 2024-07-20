import requests

BASE_URL = 'https://clickmis.net'

def create_product(user_guid, product_data):
    url = f'{BASE_URL}/api/Item/Create?userGuid={user_guid}'
    response = requests.post(url, json=product_data)
    return response.json()

def edit_product(item_guid, product_data):
    url = f'{BASE_URL}/api/Item/Edit?itemGuid={item_guid}'
    response = requests.put(url, json=product_data)
    return response.json()

def view_product(user_guid, item_guid):
    url = f'{BASE_URL}/api/Item/View?userGuid={user_guid}&itemGuid={item_guid}'
    response = requests.get(url)
    return response.json()

def list_products(user_guid, page_number, step, search):
    url = f'{BASE_URL}/api/Item/List?userGuid={user_guid}&pageNumber={page_number}&step={step}&search={search}'
    response = requests.get(url)
    return response.json()

def list_product_count(user_guid, step, search):
    url = f'{BASE_URL}/api/Item/ListCount?userGuid={user_guid}&step={step}&search={search}'
    response = requests.get(url)
    return response.json()
