import random
import requests
import json
import yaml
import numpy as np


def compute_accuracy(estimated):
    return abs(estimated - np.pi)


def compute_variance(estimator_func, func_parameters, num_runs=100, seed=None):
    estimates = np.array([estimator_func(*func_parameters, seed) for _ in range(num_runs)])
    return np.var(estimates)


def handle(seed):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed("magic number")


def read_yaml(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)
    return config


config = read_yaml(config_path := "config.yaml")


def get_qo_arev_truly_random_number():
    """ Get a truly random number from random.org"""
    url = "https://api.random.org/json-rpc/4/invoke"
    headers = {"Content-Type": "application/json"}

    payload = {
        "jsonrpc": "2.0",
        "method": "generateDecimalFractions",
        "params": {
            "apiKey": config["random_api_key"],
            "n": 1,
            "decimalPlaces": 10
        },
        "id": 42
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        if "result" in response_data and "random" in response_data["result"]:
            random_number = response_data["result"]["random"]["data"][0]
            return random_number
        else:
            raise Exception("Invalid response from random.org: {}".format(response_data))
    except Exception as e:
        raise Exception("Failed to fetch random number: {}".format(e))