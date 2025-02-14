import time
import numpy as np
from src.binomial_tree import BinomialTree
from src.monte_carlo import MonteCarloOptionPricer


def test_computation_time():
    # Test binomial tree scaling
    steps = [100, 500, 1000]
    bt_times = []
    for n in steps:
        start = time.time()
        BinomialTree(100, 100, 1, 0.05, 0.2, n).price_european('call')
        bt_times.append(time.time() - start)

    # Test Monte Carlo scaling
    sims = [1e4, 1e5, 1e6]
    mc_times = []
    for n in sims:
        start = time.time()
        MonteCarloOptionPricer(100, 100, 1, 0.05, 0.2, int(n)).price_european('call')
        mc_times.append(time.time() - start)

    # Verify linear scaling
    assert np.all(np.diff(bt_times) > 0), "Binomial tree times should increase with steps"
    assert np.all(np.diff(mc_times) > 0), "Monte Carlo times should increase with sims"

    print("\nPerformance Results:")
    print(f"Binomial Tree Times (steps={steps}): {bt_times}")
    print(f"Monte Carlo Times (sims={sims}): {mc_times}")
