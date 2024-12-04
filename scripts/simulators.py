import math
from common import *


# Pi Estimation Simulator
def estimate_pi(num_points, seed='p'):
    handle(seed)
    inside_circle = 0
    for _ in range(num_points):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return (inside_circle / num_points) * 4


def convergence_speed(iterations, threshold, printout=False):
    result = iterations
    for i in range(1000, iterations, 1000):
        error = compute_accuracy(estimate_pi(i))
        if error < threshold:
            result = i
            break

    if printout:
        print(f"Convergence speed (iterations to reach {threshold} accuracy): {result}")
    return result


# Buffon's Needle Simulator
def estimate_pi_buffon(needle_length, line_spacing, num_simulations, seed='p'):
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


def convergence_speed_buffon(iterations, needle_length=1, line_spacing=2, threshold=0.01, rng=random.random):
    if needle_length > line_spacing:
        raise ValueError("Needle length must not exceed line spacing for this implementation.")

    hits = 0
    converged_iteration = None

    for i in range(1, iterations + 1):
        d = rng() * (line_spacing / 2)
        theta = rng() * np.pi

        if d <= (needle_length / 2) * math.sin(theta):
            hits += 1

        if hits > 0:
            pi_estimate = (2 * needle_length * i) / (line_spacing * hits)
            error = abs(np.pi - pi_estimate)
        else:
            error = float('inf')

        if converged_iteration is None and error < threshold:
            converged_iteration = i

    return converged_iteration
