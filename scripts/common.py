import json
import time
import requests
import yaml
import numpy as np
import random

import scipy.stats as stats


def handle(seed):
    if seed == 'p':
        random.seed(time.time())
    else:
        random.seed(seed)


def compute_accuracy(estimated):
    return abs(estimated - np.pi)


### Statistical Tests

def perform_t_test(data1, data2, alpha=0.05, printout=True):
    t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=False)  # Welch's t-test
    decision = "Reject null hypothesis" if p_value < alpha else "Fail to reject null hypothesis"
    if printout:
        print(f"\tF-statistic: {t_stat:.4f}, P-value: {p_value:.4f}, Decision: {decision}")
    return t_stat, p_value, decision


def perform_f_test(data1, data2, alpha=0.05, printout=True):
    var1 = np.var(data1, ddof=1)
    var2 = np.var(data2, ddof=1)
    f_stat = var1 / var2 if var1 > var2 else var2 / var1
    df1, df2 = len(data1) - 1, len(data2) - 1
    p_value = 1 - stats.f.cdf(f_stat, df1, df2)
    decision = "Reject null hypothesis" if p_value < alpha else "Fail to reject null hypothesis"
    if printout:
        print(f"\tF-statistic: {f_stat:.4f}, P-value: {p_value:.4f}, Decision: {decision}")
    return f_stat, p_value, decision


###


''
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
