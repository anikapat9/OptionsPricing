import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.comparison import OptionPriceComparison
import matplotlib.pyplot as plt


def run_test_scenarios():
    comparison = OptionPriceComparison()

    # Define different scenarios
    scenarios = {
        'At the Money': {
            'S0': 100, 'K': 100, 'T': 1, 'r': 0.05, 'sigma': 0.2
        },
        'Out of the Money': {
            'S0': 90, 'K': 100, 'T': 1, 'r': 0.05, 'sigma': 0.2
        },
        'In the Money': {
            'S0': 110, 'K': 100, 'T': 1, 'r': 0.05, 'sigma': 0.2
        },
        'High Volatility': {
            'S0': 100, 'K': 100, 'T': 1, 'r': 0.05, 'sigma': 0.4
        },
        'Short Term': {
            'S0': 100, 'K': 100, 'T': 0.25, 'r': 0.05, 'sigma': 0.2
        }
    }

    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')

    for scenario_name, params in scenarios.items():
        print(f"\nTesting {scenario_name} scenario:")
        print("Parameters:", params)

        # Run comparison
        results = comparison.compare_prices(**params)

        # Create plots
        price_fig = comparison.plot_price_comparison(results)
        conv_fig = comparison.plot_convergence(**params)

        # Save plots to results directory
        price_fig.savefig(f'results/price_comparison_{scenario_name.lower().replace(" ", "_")}.png')
        conv_fig.savefig(f'results/convergence_{scenario_name.lower().replace(" ", "_")}.png')
        plt.close('all')  # Close figures to free memory

        # Print results
        print(f"\nResults for {scenario_name}:")
        print(f"Black-Scholes Call: ${results['BS_call']:.2f}")
        print(f"Monte Carlo Call: ${results['MC_call']:.2f}")
        print(f"Call 95% CI: (${results['Call_CI'][0]:.2f}, ${results['Call_CI'][1]:.2f})")
        print(f"Black-Scholes Put: ${results['BS_put']:.2f}")
        print(f"Monte Carlo Put: ${results['MC_put']:.2f}")
        print(f"Put 95% CI: (${results['Put_CI'][0]:.2f}, ${results['Put_CI'][1]:.2f})")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    run_test_scenarios()

