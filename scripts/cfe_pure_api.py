import requests
import json


BASE_URL = 'http://127.0.0.1:8000/'

ENDPOINT = 'api/updates/list/'


def get_list(id=None):
    data = json.dumps({})
    if id is not None:
        data = json.dumps({'id': id})
    r = requests.get(BASE_URL + ENDPOINT, data=data)
    print(r.status_code)
    status_code = r.status_code
    if status_code != 200:
        print('good')
    data = r.json()
    return data


def create_update():
    new_data = {
        'user': 1,
        'content': 'Some another Another user'
    }
    r = requests.post(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    print(r.headers)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()
    return r.text


def do_obj_update():
    new_data = {
        'user': '1',
        'content': 'New New New Milos Another update'
    }
    r = requests.put(BASE_URL + ENDPOINT + '16/', data=json.dumps(new_data))

    # new_data = {
    #     'id': 1,
    #     'content': 'Some Another update'
    # }
    # r = requests.put(BASE_URL + ENDPOINT, data=new_data)

    # print(r.headers)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()
    return r.text


def do_obj_delete():
    new_data = {
        'id': 12
    }
    r = requests.delete(BASE_URL + ENDPOINT + '11/', data=json.dumps(new_data))

    # new_data = {
    #     'id': 1,
    #     'content': 'Some Another update'
    # }
    # r = requests.put(BASE_URL + ENDPOINT, data=new_data)

    # print(r.headers)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()
    return r.text


# print(get_list())
# print(create_update())
# print(do_obj_update())
print(do_obj_delete())
