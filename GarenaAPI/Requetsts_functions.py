import json
import os
import time
import requests
import hashlib

STORE = os.getcwd() + "/store/"
if not os.path.isdir(STORE):
    os.mkdir(STORE)


def convert_inputs_md5(*args, **kwargs):
    """
    This function is used to check if the similar call to a function has already been made
    :param args: The args to the given function
    :param kwargs: The dictionary based arguments to a given function
    :return: The md5 value of the specific inputs to the function.
    """
    str_args = "~|~".join(args)
    str_kwargs = json.dumps(kwargs)
    combined = "ARGS:" + str_args + "|||KWARGS:" + str_kwargs
    return hashlib.md5(combined.encode()).hexdigest()


def raw_cache(func):
    """
    Automatically caches function calls so as to not repeat them. The caches are stored locally.

    This is simply a decorator.
    """
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
    """
    Write json data out to the given file.
    """
    with open(file, 'w+') as outfile:
        json.dump(data, outfile)


def read_json(file):
    with open(file) as json_file:
        return json.load(json_file)

@raw_cache
def general_data_request(endpoint, **kwargs):
    """
    Send a data request to the given API endpoint.
    :param endpoint: The endpoint for which to send the get request
    :param kwargs: The data to be passed to the requests.get() method.
    :return: the data retrieved from the remote endpoint.
    """
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
