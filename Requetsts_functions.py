import json
import os
import time
import requests
import hashlib

STORE = os.getcwd() + "/store/"
if not os.path.isdir(STORE):
    os.mkdir(STORE)


def convert_inputs_md5(*args, **kwargs):
    str_args = "~|~".join(args)
    str_kwargs = json.dumps(kwargs)
    combined = "ARGS:" + str_args + "|||KWARGS:" + str_kwargs
    return hashlib.md5(combined.encode()).hexdigest()


def raw_cache(func):
    def wrapper(*args, **kwargs):
        location = STORE + func.__name__ + "/"
        if not os.path.isdir(location):
            os.mkdir(location)

        file_name = convert_inputs_md5(*args, **kwargs)

        if file_name in os.listdir(location):
            return read_json(location + file_name)
        else:
            data = func(*args, **kwargs)
            write_json(location + file_name, data)
            return data

    return wrapper


def write_json(file, data):
    with open(file, 'w+') as outfile:
        json.dump(data, outfile)


def read_json(file):
    with open(file) as json_file:
        return json.load(json_file)

@raw_cache
def general_data_request(endpoint, **kwargs):
    request = requests.get(endpoint, **kwargs)
    if request.status_code == 200:
        return request.json()
    if request.status_code == 429:
        print("Too many requests. Delaying execution.")
        time.sleep(1)
        return general_data_request(endpoint, **kwargs)
    else:
        print(kwargs)
        print(request.status_code)
        raise ValueError
