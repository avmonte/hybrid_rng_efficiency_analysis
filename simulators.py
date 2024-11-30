import math
import random
import numpy as np
from common import *


# Pi Estimation Simulator
def estimate_pi(num_points, seed=None):
    handle(seed)
    inside_circle = 0
    for _ in range(num_points):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return (inside_circle / num_points) * 4


def convergence_speed(iterations, threshold, seed=None):
    for i in range(1000, iterations, 1000):
        error = compute_accuracy(estimate_pi(i, seed))
        if error < threshold:
            return i

    return iterations


# Buffon's Needle Simulator
def estimate_pi_buffon(needle_length, line_spacing, num_simulations, seed=None):
    handle(seed)
    if needle_length > line_spacing:
        raise ValueError("Needle length must be less than or equal to line spacing.")

    crosses = 0
    for _ in range(num_simulations):
        center = random.uniform(0, line_spacing / 2)
        angle = random.uniform(0, np.pi)
        tip_distance = (needle_length / 2) * math.sin(angle)
        if center <= tip_distance:
            crosses += 1

    if crosses == 0:
        return float('inf')
    estimate = (2 * needle_length * num_simulations) / (line_spacing * crosses)
    return estimate
