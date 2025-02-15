# Options Pricing Models

A Python-based project implementing financial options pricing models, including Black-Scholes, Monte Carlo simulation, and Binomial Tree methods. This repository also supports scenario testing, visualization, and performance analysis.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Examples](#examples)
7. [Known Issues & Limitations](#known-issues--limitations)
8. [Contributing](#contributing)
9. [License](#license)

---

## **Introduction**
This project provides tools to calculate the prices of financial options using three popular methods:
- **Black-Scholes Model** for analytical pricing of European options.
- **Monte Carlo Simulation** for numerical pricing with variance reduction techniques.
- **Binomial Tree Model** for pricing both European and American options.

The goal is to provide a flexible framework for understanding and comparing these methods under different market conditions.

---

## **Features**
- Pricing models:
  - Black-Scholes (Analytical)
  - Monte Carlo Simulation
  - Binomial Tree (Supports American options)
- Scenario Testing:
  - Predefined scenarios to validate model accuracy.
- Visualization:
  - Convergence plots for Monte Carlo and Binomial Tree methods.
  - Comparison charts for different pricing methods.
- Stress Testing:
  - Performance analysis with increasing steps/simulations.
- Exotic Options:
  - Support for Asian and Barrier options.

---

## **Technologies Used**
- Python 3.10+
- Libraries:
  - `numpy` (Numerical computations)
  - `scipy` (Statistical functions)
  - `matplotlib` (Visualization)
  - `pandas` (Data handling)

---

## **Installation**
1. Clone the repository
2. Install dependencies

For custom parameters, modify the test files or create your own scripts using the classes in the `src/` directory.

---

## **Examples**

### Scenario Testing Output:
| Scenario              | Call Prices (BS / MC / BT) | Put Prices (BS / MC / BT) |
|-----------------------|---------------------------|---------------------------|
| At the Money          | $10.45 / $10.42 / $10.43 | $5.57 / $5.57 / $5.55     |
| Out of the Money      | $5.09 / $5.10 / $5.10    | $10.21 / $10.22 / $10.23  |
| In the Money          | $17.66 / $17.64 / $17.68 | $2.79 / $2.79 / $2.80     |

---

## **Issues & Limitations**
1. Black-Scholes and Monte Carlo methods do not support American options.
2. Monte Carlo results may vary slightly due to randomness; increase simulations (`n_sims`) for better accuracy.
3. Exotic options like Barrier or Lookback are partially implemented.

---

## **License**
This project is licensed under the MIT License.

---

