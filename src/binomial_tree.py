import numpy as np


class BinomialTree:
    def __init__(self, S0, K, T, r, sigma, n_steps=100):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.n = n_steps
        self.dt = T / n_steps
        self.u = np.exp(sigma * np.sqrt(self.dt))
        self.d = 1 / self.u
        self.p = (np.exp(r * self.dt) - self.d) / (self.u - self.d)

    def price_european(self, option_type='call'):
        stock = self.S0 * self.u ** (np.arange(self.n, -1, -1)) * self.d ** np.arange(0, self.n + 1)
        option = np.maximum(stock - self.K, 0) if option_type == 'call' else np.maximum(self.K - stock, 0)

        for _ in range(self.n, 0, -1):
            option = np.exp(-self.r * self.dt) * (self.p * option[:-1] + (1 - self.p) * option[1:])

        return option[0]

    def price_american(self, option_type='put'):
        stock_tree = np.zeros((self.n + 1, self.n + 1))
        option_tree = np.zeros_like(stock_tree)

        # Build stock price tree
        for i in range(self.n + 1):
            for j in range(i + 1):
                stock_tree[j, i] = self.S0 * self.u ** j * self.d ** (i - j)

        # Terminal payoff
        option_tree[:, -1] = np.maximum(stock_tree[:, -1] - self.K, 0) if option_type == 'call' else \
            np.maximum(self.K - stock_tree[:, -1], 0)

        # Backward induction with early exercise
        for i in range(self.n - 1, -1, -1):
            for j in range(i + 1):
                hold = np.exp(-self.r * self.dt) * (
                            self.p * option_tree[j, i + 1] + (1 - self.p) * option_tree[j + 1, i + 1])
                exercise = stock_tree[j, i] - self.K if option_type == 'call' else self.K - stock_tree[j, i]
                option_tree[j, i] = np.maximum(hold, exercise)

        return option_tree[0, 0]
