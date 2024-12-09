import json
import time
import requests
import yaml
import numpy as np
import random

import scipy.stats as stats

DEBUG = True


def handle(rng, seed):
    if seed == 'c':
        rng.seed(time.time())
        return
    rng.seed(seed)


def are_we_there_yet(estimated):
    return abs(estimated - np.pi)


### Statistical Tests

def perform_t_test(data1, data2, alpha=0.05, printout=DEBUG):
    t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=False)  # Welch's t-test
    decision = "Reject null hypothesis" if p_value < alpha else "Fail to reject null hypothesis"
    if printout:
        print(f"\tF-statistic: {t_stat:.4f}, P-value: {p_value:.4f}, Decision: {decision}")
    return t_stat, p_value, decision


def perform_f_test(data1, data2, alpha=0.05, printout=DEBUG):
    var1 = np.var(data1, ddof=1)
    var2 = np.var(data2, ddof=1)
    f_stat = var1 / var2 if var1 > var2 else var2 / var1
    df1, df2 = len(data1) - 1, len(data2) - 1
    p_value = 1 - stats.f.cdf(f_stat, df1, df2)
    decision = "Reject null hypothesis" if p_value < alpha else "Fail to reject null hypothesis"
    if printout:
        print(f"\tF-statistic: {f_stat:.4f}, P-value: {p_value:.4f}, Decision: {decision}")
    return f_stat, p_value, decision


### True Entropy


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


def lcg(seed, a=1664525, c=1013904223, m=2**32):
    while True:
        seed = (a * seed + c) % m
        yield seed



def monte_carlo_pi_convergence(sources, labels, num_samples=10000):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure(figsize=(10, 6))
    for source, label in zip(sources, labels):
        inside_circle = 0
        pi_estimates = []
        for i in range(1, num_samples + 1):
            x, y = next(source), next(source)
            if x**2 + y**2 <= 1:
                inside_circle += 1
            pi_estimates.append((inside_circle / i) * 4)
        plt.plot(range(num_samples), pi_estimates, label=label)
    plt.axhline(np.pi, color='black', linestyle='--', label="True π")
    plt.title("Monte Carlo π Convergence")
    plt.xlabel("Iterations")
    plt.ylabel("Estimated π")
    plt.legend()
    plt.show()



def plot_uniformity_comparison(sources, labels, num_samples=10000):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    for source, label in zip(sources, labels):
        values = [next(source) for _ in range(num_samples)]
        plt.hist(values, bins=20, alpha=0.6, label=label, density=True)
    plt.title("Uniformity Comparison")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()


def plot_autocorrelation_comparison(sources, labels, num_samples=10000):
    import numpy as np
    import matplotlib.pyplot as plt
    autocorrelations = []
    for source in sources:
        values = [next(source) for _ in range(num_samples)]
        autocorr = np.corrcoef(values[:-1], values[1:])[0, 1]
        autocorrelations.append(autocorr)

    plt.bar(labels, autocorrelations, color=['red', 'green', 'blue'])
    plt.title("Lag-1 Autocorrelation Comparison")
    plt.ylabel("Autocorrelation")
    plt.show()

def buffon_pi_comparison(sources, labels, num_needles=10000):
    import numpy as np

    estimates = []
    for source in sources:
        hits = 0
        line_distance = 1
        needle_length = 0.5
        for _ in range(num_needles):
            x = next(source) * line_distance / 2
            theta = next(source) * np.pi
            if x <= needle_length / 2 * np.sin(theta):
                hits += 1
        pi_estimate = (2 * needle_length * num_needles) / (hits * line_distance)
        estimates.append(pi_estimate)

    # Bar plot of estimates
    import matplotlib.pyplot as plt
    plt.bar(labels, estimates, color=['red', 'green', 'blue'])
    plt.axhline(np.pi, color='black', linestyle='--', label="True π")
    plt.title("Buffon's Needle π Estimation")
    plt.ylabel("Estimated π")
    plt.legend()
    plt.show()