import numpy as np
from scipy.stats import norm
import yfinance as yf
from datetime import datetime, timedelta


class BlackScholes:
    def __init__(self):
        self.S = None  # Stock price
        self.K = None  # Strike price
        self.T = None  # Time to maturity (in years)
        self.r = None  # Risk-free rate
        self.sigma = None  # Volatility

    def calculate_price(self, S, K, T, r, sigma, option_type='call'):
        """
        Calculate option price using Black-Scholes formula

        Parameters:
        -----------
        S : float
            Current stock price
        K : float
            Strike price
        T : float
            Time to maturity (in years)
        r : float
            Risk-free rate (decimal form, e.g., 0.05 for 5%)
        sigma : float
            Volatility (decimal form, e.g., 0.2 for 20%)
        option_type : str
            'call' or 'put'
        """
        self.S, self.K, self.T, self.r, self.sigma = S, K, T, r, sigma

        d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return price

    def calculate_greeks(self, option_type='call'):
        """Calculate option Greeks"""
        d1 = (np.log(self.S / self.K) + (self.r + self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)

        # Delta
        if option_type == 'call':
            delta = norm.cdf(d1)
        else:
            delta = -norm.cdf(-d1)

        # Gamma (same for calls and puts)
        gamma = norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))

        # Theta
        theta = -self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T))
        if option_type == 'call':
            theta -= self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        else:
            theta += self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)

        # Vega (same for calls and puts)
        vega = self.S * np.sqrt(self.T) * norm.pdf(d1)

        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta / 365,  # Daily theta
            'vega': vega / 100  # Vega per 1% change in volatility
        }

    @staticmethod
    def get_historical_volatility(ticker, lookback_days=252):
        """Calculate historical volatility from market data"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_days)

            # Download historical data
            stock = yf.download(ticker, start=start_date, end=end_date)

            # Calculate daily returns
            returns = np.log(stock['Close'] / stock['Close'].shift(1))

            # Calculate annualized volatility
            volatility = returns.std() * np.sqrt(252)

            return volatility

        except Exception as e:
            print(f"Error calculating historical volatility: {str(e)}")
            return None


if __name__ == "__main__":
    # Example usage
    bs = BlackScholes()

    # Example parameters
    S = 100  # Stock price
    K = 100  # Strike price
    T = 1  # One year to expiration
    r = 0.05  # 5% risk-free rate
    sigma = 0.2  # 20% volatility

    # Calculate call and put prices
    call_price = bs.calculate_price(S, K, T, r, sigma, 'call')
    put_price = bs.calculate_price(S, K, T, r, sigma, 'put')

    print(f"Call Option Price: ${call_price:.2f}")
    print(f"Put Option Price: ${put_price:.2f}")

    # Calculate and display Greeks
    greeks = bs.calculate_greeks('call')
    print("\nOption Greeks:")
    for greek, value in greeks.items():
        print(f"{greek.capitalize()}: {value:.4f}")

    # Example of calculating historical volatility
    ticker = "AAPL"
    hist_vol = bs.get_historical_volatility(ticker)
    if hist_vol:
        print(f"\nHistorical Volatility for {ticker}: {hist_vol:.2%}")
