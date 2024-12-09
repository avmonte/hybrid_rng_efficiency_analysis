import matplotlib.pyplot as plt
from scripts.common import *

DEBUG = True


# Pi Estimation Simulator
def estimate_pi(num_points, rng=random, seed='c'):
    """
    :param num_points:
    :param seed:
    :param rng: must return a random number in the range [0, 1)
    """

    handle(rng, seed)

    inside_circle = 0
    for _ in range(num_points):
        x, y = rng.random(), rng.random()
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return (inside_circle / num_points) * 4


def convergence_speed(max_simulations, threshold, step=100, rng=random, printout=DEBUG):
    result = max_simulations
    for i in range(step, max_simulations, step):
        error = are_we_there_yet(estimate_pi(i, rng))
        if error < threshold:
            result = i
            break

    if printout:
        print(f"Convergence speed (iterations to reach {threshold} accuracy): {result}")
    return result


# Buffon's Needle Simulator
def estimate_pi_buffon(needle_length, line_spacing, num_needles, seed='c', rng=random):
    if seed == 'c':
        rng.seed(time.time())
    else:
        rng.seed(seed)
    if needle_length > line_spacing:
        raise ValueError("Needle length must be less than or equal to line spacing.")

    crosses = 0
    for _ in range(num_needles):
        center = rng.uniform(0, line_spacing / 2)
        angle = rng.uniform(0, np.pi)
        tip_distance = (needle_length / 2) * np.sin(angle)
        if center <= tip_distance:
            crosses += 1

    if crosses == 0:
        return float('inf')
    estimate = (2 * needle_length * num_needles) / (line_spacing * crosses)
    return estimate


def plot_buffon_convergence(length_of_needles, spacing, estimate_pi_buffon, max_needles=1000000):

    # Define number of needles for each simulation
    needle_counts = np.logspace(1, np.log10(max_needles), num=1000, dtype=int)

    errors = []
    errors_orig = []

    # Compute the absolute error for each needle count
    for n in needle_counts:
        pi_estimate = np.median([estimate_pi_buffon(length_of_needles, spacing, n, rng=lcg) for _ in range(10)])
        pi_estimate_orig = np.median([estimate_pi_buffon(length_of_needles, spacing, n) for _ in range(10)])

        errors.append(are_we_there_yet(pi_estimate))
        errors_orig.append(are_we_there_yet(pi_estimate_orig))

    # Plot the results
    plt.figure(figsize=(8, 6))
    plt.loglog(needle_counts, errors, label="Buffon's Needle Error: LCG")
    plt.loglog(needle_counts, errors_orig, label="Buffon's Needle Error: Random")
    plt.loglog(needle_counts, 1 / np.sqrt(needle_counts), label="1 / sqrt(N) (Expected)", linestyle="--")
    plt.xlabel("Number of Needles")
    plt.ylabel("Absolute Error")
    plt.title("Convergence Rate of Buffon's Needle Experiment")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()
