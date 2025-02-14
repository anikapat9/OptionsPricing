# examples/usage.py
from src.comparison import OptionAnalysis

if __name__ == "__main__":
    analyzer = OptionAnalysis()

    # Basic comparison
    print(analyzer.full_comparison(
        S0=100, K=100, T=1, r=0.05, sigma=0.2,
        n_steps=500, n_sims=100000
    ))

    # Convergence analysis plot
    fig = analyzer.plot_convergence()
    fig.savefig('convergence_analysis.png')
