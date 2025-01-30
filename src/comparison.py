import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.black_scholes import BlackScholes
from src.monte_carlo import MonteCarloOptionPricer


class OptionPriceComparison:
    def __init__(self):
        self.bs_model = BlackScholes()
        plt.style.use('seaborn-v0_8')

    def compare_prices(self, S0, K, T, r, sigma, n_simulations=10000):
        # Previous comparison code remains the same
        bs_call = self.bs_model.calculate_price(S0, K, T, r, sigma, 'call')
        bs_put = self.bs_model.calculate_price(S0, K, T, r, sigma, 'put')

        mc_pricer = MonteCarloOptionPricer(S0, K, T, r, sigma, n_simulations)
        mc_call = mc_pricer.price_european_call()
        mc_put = mc_pricer.price_european_put()

        call_ci = mc_pricer.calculate_confidence_interval('call')
        put_ci = mc_pricer.calculate_confidence_interval('put')

        return {
            'BS_call': bs_call,
            'MC_call': mc_call,
            'Call_CI': call_ci,
            'BS_put': bs_put,
            'MC_put': mc_put,
            'Put_CI': put_ci
        }

    def plot_price_comparison(self, results):
        """Plot bar chart comparing BS and MC prices"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Call options comparison
        methods = ['Black-Scholes', 'Monte Carlo']
        call_prices = [results['BS_call'], results['MC_call']]
        ax1.bar(methods, call_prices, color=['lightblue', 'lightgreen'])
        ax1.set_title('Call Option Price Comparison')
        ax1.set_ylabel('Option Price ($)')

        # Add confidence interval for Monte Carlo
        # Calculate absolute errors for error bars
        call_lower_err = abs(results['MC_call'] - results['Call_CI'][0])
        call_upper_err = abs(results['Call_CI'][1] - results['MC_call'])
        ax1.errorbar(x=1, y=results['MC_call'],
                     yerr=[[call_lower_err], [call_upper_err]],
                     color='black', capsize=5)

        # Put options comparison
        put_prices = [results['BS_put'], results['MC_put']]
        ax2.bar(methods, put_prices, color=['lightblue', 'lightgreen'])
        ax2.set_title('Put Option Price Comparison')
        ax2.set_ylabel('Option Price ($)')

        # Add confidence interval for Monte Carlo
        put_lower_err = abs(results['MC_put'] - results['Put_CI'][0])
        put_upper_err = abs(results['Put_CI'][1] - results['MC_put'])
        ax2.errorbar(x=1, y=results['MC_put'],
                     yerr=[[put_lower_err], [put_upper_err]],
                     color='black', capsize=5)

        plt.tight_layout()
        return fig

    def plot_convergence(self, S0, K, T, r, sigma, max_sims=100000, steps=20):
        """Plot Monte Carlo convergence to Black-Scholes price"""
        # Calculate BS price once
        bs_price = self.bs_model.calculate_price(S0, K, T, r, sigma, 'call')

        # Generate different numbers of simulations
        sim_numbers = np.linspace(1000, max_sims, steps, dtype=int)
        mc_prices = []
        confidence_intervals = []

        for n_sim in sim_numbers:
            mc_pricer = MonteCarloOptionPricer(S0, K, T, r, sigma, n_sim)
            mc_price = mc_pricer.price_european_call()
            ci = mc_pricer.calculate_confidence_interval('call')
            mc_prices.append(mc_price)
            confidence_intervals.append(ci)

        # Create convergence plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot MC prices
        ax.plot(sim_numbers, mc_prices, label='Monte Carlo', color='green')

        # Plot BS price as horizontal line
        ax.axhline(y=bs_price, color='blue', linestyle='--',
                   label='Black-Scholes')

        # Plot confidence intervals
        ci_lower = [ci[0] for ci in confidence_intervals]
        ci_upper = [ci[1] for ci in confidence_intervals]
        ax.fill_between(sim_numbers, ci_lower, ci_upper,
                        alpha=0.2, color='green')

        ax.set_xlabel('Number of Simulations')
        ax.set_ylabel('Option Price ($)')
        ax.set_title('Monte Carlo Price Convergence')
        ax.legend()

        return fig


if __name__ == "__main__":
    # Test the visualizations
    comparison = OptionPriceComparison()

    # Compare prices
    results = comparison.compare_prices(
        S0=100,  # Current stock price
        K=100,  # Strike price
        T=1,  # Time to maturity
        r=0.05,  # Risk-free rate
        sigma=0.2  # Volatility
    )

    # Create and save price comparison plot
    price_fig = comparison.plot_price_comparison(results)
    price_fig.savefig('price_comparison.png')

    # Create and save convergence plot
    conv_fig = comparison.plot_convergence(
        S0=100, K=100, T=1, r=0.05, sigma=0.2
    )
    conv_fig.savefig('convergence.png')

    print("Plots have been saved!")
