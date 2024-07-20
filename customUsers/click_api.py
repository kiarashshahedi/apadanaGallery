import requests

BASE_URL = 'https://clickmis.net'

def login(username, password, mac_address, otp):
    url = f'{BASE_URL}/api/User/Login'
    payload = {
        "UserName": username,
        "Password": password,
        "MacAddress": mac_address,
        "OTP": otp
    }
    response = requests.post(url, json=payload)
    return response.json()

def register(first_name, last_name, mobile_phone, otp, is_demo):
    url = f'{BASE_URL}/api/User/Register'
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "mobilePhone": mobile_phone,
        "otp": otp,
        "isDemo": is_demo
    }
    response = requests.post(url, json=payload)
    return response.json()

def update_user(user_guid, status):
    url = f'{BASE_URL}/api/User/UpdateUser?userGuid={user_guid}&status={status}'
    response = requests.get(url)
    return response.json()

def get_user_info(user_guid):
    url = f'{BASE_URL}/api/User/Info?userGuid={user_guid}'
    response = requests.get(url)
    return response.json()

def change_password(user_guid, previous_password, new_password):
    url = f'{BASE_URL}/api/User/ChangePassword'
    payload = {
        "UserGuid": user_guid,
        "PreviousPassword": previous_password,
        "NewPassword": new_password
    }
    response = requests.post(url, json=payload)
    return response.json()

def get_user_group_list(user_guid):
    url = f'{BASE_URL}/api/User/UserGroupList?userGuid={user_guid}'
    response = requests.get(url)
    return response.json()

def get_user_list(user_guid, page_number, step, search):
    url = f'{BASE_URL}/api/User/List?userGuid={user_guid}&pageNumber={page_number}&step={step}&search={search}'
    response = requests.get(url)
    return response.json()

def get_user_list_count(user_guid, step, search):
    url = f'{BASE_URL}/api/User/ListCount?userGuid={user_guid}&step={step}&search={search}'
    response = requests.get(url)
    return response.json()

def register_from_site(first_name, last_name, mobile_phone, otp, is_demo):
    url = f'{BASE_URL}/api/User/RegisterFromSite'
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "mobilePhone": mobile_phone,
        "otp": otp,
        "isDemo": is_demo
    }
    response = requests.post(url, json=payload)
    return response.json()
