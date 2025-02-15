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
        """Plot Monte Carlo and Binomial Tree convergence to Black-Scholes price."""
        steps = np.arange(10, 500, 10)
        bt_prices = [BinomialTree(S0, K, T, r, sigma, n).price_european('call') for n in steps]
        mc_prices = [MonteCarloOptionPricer(S0, K, T, r, sigma, n).price_european('call')
                     for n in [100, 500, 1000, 5000, 10000]]
        bs_price = self.bs.calculate_price(S0, K, T, r, sigma, 'call')

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot Binomial Tree prices
        ax.plot(steps, bt_prices, label='Binomial Tree (Steps)', color='blue', linestyle='-')

        # Plot Monte Carlo prices
        mc_steps = [100, 500, 1000, 5000, 10000]
        ax.scatter(mc_steps, mc_prices, label='Monte Carlo (Simulations)', color='green')

        # Plot Black-Scholes price as a horizontal line
        ax.axhline(y=bs_price, color='red', linestyle='--', label=f'Black-Scholes Price (${bs_price:.2f})')

        # Add titles and labels
        ax.set_title('Convergence of Pricing Methods', fontsize=14)
        ax.set_xlabel('Number of Steps/Simulations', fontsize=12)
        ax.set_ylabel('Option Price ($)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True)

        return fig


