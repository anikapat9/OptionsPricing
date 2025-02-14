from src.comparison import OptionAnalysis
import matplotlib.pyplot as plt


def run_test_scenarios():
    comparison = OptionAnalysis()
    # Test scenarios
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

    for name, params in scenarios.items():
        print(f"\nTesting {name} scenario:")
        print("Parameters:", params)

        # Run comparison
        results = comparison.compare_all_methods(**params)

        # Create and save plot
        fig = comparison.plot_comparison(results)
        plt.savefig(f'results/comparison_{name.lower().replace(" ", "_")}.png')
        plt.close()

        # Print results
        print("\nCall Options:")
        for method, price in results['Call Options'].items():
            print(f"{method}: ${price:.2f}")

        print("\nPut Options:")
        for method, price in results['Put Options'].items():
            print(f"{method}: ${price:.2f}")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    run_test_scenarios()
