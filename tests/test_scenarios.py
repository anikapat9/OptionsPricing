import numpy as np

from src.comparison import OptionAnalysis
import matplotlib.pyplot as plt
import os


def run_test_scenarios():
    comparison = OptionAnalysis()

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

        # Run comparison using full_comparison()
        results = comparison.full_comparison(**params)

        # Create and save plot (if needed)
        fig = comparison.plot_convergence(**params)
        fig.savefig(f'results/convergence_{scenario_name.lower().replace(" ", "_")}.png')
        plt.close('all')  # Close figures to free memory

        # Print results
        print("\nCall Options:")
        for method, price in results['European Call'].items():
            print(f"{method}: ${price:.2f}")

        print("\nPut Options:")
        for method, price in results['European Put'].items():
            print(f"{method}: ${price:.2f}")

        if "American Put" in results:
            print("\nAmerican Put:")
            for method, price in results['American Put'].items():
                if np.isnan(price):
                    print(f"{method}: Not applicable")
                else:
                    print(f"{method}: ${price:.2f}")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    run_test_scenarios()

