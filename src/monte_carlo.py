import numpy as np
from scipy.stats import norm
import yfinance as yf


class MonteCarloOptionPricer:
    def __init__(self, S0, K, T, r, sigma, n_simulations=10000):
        self.S0 = S0  # Initial stock price
        self.K = K  # Strike price
        self.T = T  # Time to maturity
        self.r = r  # Risk-free rate
        self.sigma = sigma  # Volatility
        self.n_sim = n_simulations

    def simulate_paths(self):
        """Generate stock price paths using geometric Brownian motion"""
        dt = self.T
        Z = np.random.standard_normal(self.n_sim)
        ST = self.S0 * np.exp((self.r - 0.5 * self.sigma ** 2) * dt +
                              self.sigma * np.sqrt(dt) * Z)
        return ST

    def price_european_call(self):
        """Calculate European call option price"""
        ST = self.simulate_paths()
        payoffs = np.maximum(ST - self.K, 0)
        option_price = np.exp(-self.r * self.T) * np.mean(payoffs)
        return option_price

    def price_european_put(self):
        """Calculate European put option price"""
        ST = self.simulate_paths()
        payoffs = np.maximum(self.K - ST, 0)
        option_price = np.exp(-self.r * self.T) * np.mean(payoffs)
        return option_price

    def calculate_confidence_interval(self, option_type='call', confidence=0.95):
        """Calculate confidence interval for option price"""
        if option_type == 'call':
            ST = self.simulate_paths()
            payoffs = np.maximum(ST - self.K, 0)
        else:
            ST = self.simulate_paths()
            payoffs = np.maximum(self.K - ST, 0)

        discounted_payoffs = np.exp(-self.r * self.T) * payoffs
        mean_price = np.mean(discounted_payoffs)
        std_error = np.std(discounted_payoffs) / np.sqrt(self.n_sim)
        z_score = norm.ppf((1 + confidence) / 2)

        return (mean_price - z_score * std_error,
                mean_price + z_score * std_error)


if __name__ == "__main__":
    # Example usage
    mc_pricer = MonteCarloOptionPricer(
        S0=100,  # Current stock price
        K=100,  # Strike price
        T=1,  # One year to expiration
        r=0.05,  # 5% risk-free rate
        sigma=0.2,  # 20% volatility
        n_simulations=100000
    )

    call_price = mc_pricer.price_european_call()
    put_price = mc_pricer.price_european_put()
    confidence_interval = mc_pricer.calculate_confidence_interval()

    print(f"Monte Carlo Call Price: ${call_price:.2f}")
    print(f"Monte Carlo Put Price: ${put_price:.2f}")
    print(f"95% Confidence Interval: (${confidence_interval[0]:.2f}, ${confidence_interval[1]:.2f})")
