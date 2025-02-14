# src/comparison.py (updated)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .black_scholes import BlackScholes
from .monte_carlo import MonteCarloOptionPricer
from .binomial_tree import BinomialTree

plt.style.use('ggplot')


class OptionAnalysis:
    def __init__(self):
        self.bs = BlackScholes()

    def full_comparison(self, S0, K, T, r, sigma, n_steps=100, n_sims=100000):
        results = {
            'European Call': {
                'BS': self.bs.calculate_price(S0, K, T, r, sigma, 'call'),
                'MC': MonteCarloOptionPricer(S0, K, T, r, sigma, n_sims).price_european('call'),
                'BT': BinomialTree(S0, K, T, r, sigma, n_steps).price_european('call')
            },
            'European Put': {
                'BS': self.bs.calculate_price(S0, K, T, r, sigma, 'put'),
                'MC': MonteCarloOptionPricer(S0, K, T, r, sigma, n_sims).price_european('put'),
                'BT': BinomialTree(S0, K, T, r, sigma, n_steps).price_european('put')
            },
            'American Put': {
                'BT': BinomialTree(S0, K, T, r, sigma, n_steps).price_american('put')
            }
        }
        return pd.DataFrame(results)

    def plot_convergence(self, S0=100, K=100, T=1, r=0.05, sigma=0.2):
        steps = np.arange(10, 500, 10)
        bt_prices = [BinomialTree(S0, K, T, r, sigma, n).price_european('call') for n in steps]
        mc_prices = [MonteCarloOptionPricer(S0, K, T, r, sigma, n).price_european('call')
                     for n in [100, 500, 1000, 5000, 10000, 50000, 100000]]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(steps, bt_prices, label='Binomial Tree')
        ax.plot([10, 100, 500, 1000, 5000, 10000, 50000, 100000],
                [self.bs.calculate_price(S0, K, T, r, sigma, 'call')] * 8,
                'r--', label='Black-Scholes')
        ax.set(xlabel='Number of Steps/Simulations', ylabel='Call Price',
               title='Convergence of Pricing Methods')
        ax.legend()
        return fig

