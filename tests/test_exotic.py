import numpy as np
from src.monte_carlo import MonteCarloOptionPricer
from src.binomial_tree import BinomialTree
from src.black_scholes import BlackScholes


def test_asian_options():
    # Test Asian call options
    mc = MonteCarloOptionPricer(S0=100, K=100, T=1, r=0.05, sigma=0.2, n_simulations=100000)
    asian_price = mc.price_asian(option_type='call', n_steps=252)

    # Compare with control variate method (expected value from Black-Scholes)
    bs_price = BlackScholes().calculate_price(100, 100, 1, 0.05, 0.2, 'call')
    assert np.isclose(asian_price, bs_price, rtol=0.05), \
        f"Asian price {asian_price} not close to BS {bs_price}"


def test_american_put():
    # Test American put early exercise premium
    bt = BinomialTree(S0=100, K=100, T=1, r=0.05, sigma=0.2, n_steps=500)
    american_put = bt.price_american('put')
    european_put = bt.price_european('put')

    assert american_put > european_put, \
        "American put should have higher value due to early exercise"
    assert np.isclose(american_put, 5.85, rtol=0.1), \
        f"American put price {american_put} outside expected range"


def test_barrier_options():
    # Test up-and-out call option
    n_sims = 100000
    barrier = 110
    mc = MonteCarloOptionPricer(S0=100, K=100, T=1, r=0.05, sigma=0.2, n_simulations=n_sims)
    paths = mc._generate_paths(antithetic=False)  # Get actual paths

    # Barrier condition
    payoff = np.where(paths.max(axis=0) < barrier,
                      np.maximum(paths[-1] - 100, 0),
                      0)
    barrier_price = np.exp(-0.05) * payoff.mean()

    # Compare with theoretical value for barrier options
    expected_price = 4.32  # From closed-form solution
    assert np.isclose(barrier_price, expected_price, rtol=0.1), \
        f"Barrier price {barrier_price} not close to expected {expected_price}"
