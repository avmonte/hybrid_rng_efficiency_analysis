import json
import requests
import yaml
import numpy as np


def compute_accuracy(estimated):
    return abs(estimated - np.pi)


def compute_variance(estimator_func, func_parameters, num_runs=100, printout=False):
    estimates = np.array([estimator_func(*func_parameters) for _ in range(num_runs)])
    variance = np.var(estimates)

    if printout:
        print(f"Variance across {num_runs} runs: {variance:.2e}")
    return variance


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
