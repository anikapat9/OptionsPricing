# src/monte_carlo.py (updated)
import numpy as np
from scipy.stats import norm


class MonteCarloOptionPricer:
    def __init__(self, S0, K, T, r, sigma, n_simulations=10000):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.n_sim = n_simulations

    def _generate_paths(self, antithetic=True):
        Z = norm.rvs(size=self.n_sim)
        if antithetic:
            Z = np.concatenate([Z, -Z])
        ST = self.S0 * np.exp((self.r - 0.5 * self.sigma ** 2) * self.T +
                              self.sigma * np.sqrt(self.T) * Z)
        return ST

    def price_european(self, option_type='call'):
        ST = self._generate_paths()
        payoffs = np.maximum(ST - self.K, 0) if option_type == 'call' else np.maximum(self.K - ST, 0)
        price = np.exp(-self.r * self.T) * np.mean(payoffs)
        return price

    def price_asian(self, option_type='call', n_steps=100):
        dt = self.T / n_steps
        Z = norm.rvs(size=(n_steps, self.n_sim))
        S = np.zeros((n_steps + 1, self.n_sim))
        S[0] = self.S0

        for t in range(1, n_steps + 1):
            S[t] = S[t - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * dt +
                                     self.sigma * np.sqrt(dt) * Z[t - 1])

        avg_price = S.mean(axis=0)
        payoffs = np.maximum(avg_price - self.K, 0) if option_type == 'call' else np.maximum(self.K - avg_price, 0)
        return np.exp(-self.r * self.T) * np.mean(payoffs)
