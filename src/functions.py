import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from scipy.stats import norm


class Portfolio:

    def __init__(self, tickers, weights, start, end=None, portfolio_inicial_value=100000000, normalize_weights=True):
        # Modify dates
        start = datetime.strptime(start, "%Y-%m-%d")
        time = start - timedelta(days=365)
        end = datetime.today() if end is None else pd.to_datetime(end)

        # Download datas
        data = yf.download(tickers, start=time, end=end, auto_adjust=False)[['Adj Close', 'Volume']]
        prices = data['Adj Close']
        volumes = data['Volume']
        weights = pd.Series(weights, index=tickers)
        first_date_start = data.index[data.index >= start][0]

        # Identifies invalid tickers (without datas in API)
        invalid_tickers = [x for x in prices.columns if prices[x].isnull().all()]
        if len(invalid_tickers) > 0:
            # Valid Tickers
            valid_tickers = [x for x in prices.columns if not prices[x].isnull().all()]
            prices = prices[valid_tickers]
            volumes = volumes[valid_tickers]
            # Adjust Weights
            weights = weights.loc[valid_tickers]
            # Invalid Message
            print(f"Attention - Invalid Tickers({len(invalid_tickers)}):\n", invalid_tickers,"\n")

        # Normalize weights
        if normalize_weights:
            weights = weights / weights.sum()

        # Positions quantity
        positions_qty = (weights * portfolio_inicial_value / prices.iloc[0]).astype(int)

        # Returns Tickers
        all_returns_tickers = prices.pct_change(fill_method=None).fillna(0)
        returns_tickers = all_returns_tickers.loc[first_date_start:]

        # first line to return =1
        index_start = first_date_start - timedelta(days=1)
        first_line = pd.Series([0], index=[index_start])

        # Returns portfolio
        all_returns = (all_returns_tickers * weights).sum(axis=1)
        returns = all_returns.loc[first_date_start:]
        returns = pd.concat([first_line, returns])

        # Portfolio returns accumulate
        returns_accumulate = (1 + returns).cumprod() -1
        portfolio_nav = (1 + returns_accumulate) * portfolio_inicial_value

        # Atributes
        self.returns_accumulate = returns_accumulate
        self.portfolio_nav = portfolio_nav
        self.__start = time
        self.__end = end
        self.__positions = positions_qty
        self.__inicial_value = portfolio_inicial_value
        self.__volume = volumes
        self.__weights = weights
        self.__all_returns_tickers = all_returns_tickers
        self.__returns_tickers = returns_tickers
        self.__all_returns = all_returns
        self.__returns = returns
        self.__prices = prices


    def volatility_sharpe(self, volatility_window=21, volatility_standardize=252):

        # Vol window
        vol_window = self.__returns.rolling(window=volatility_window).std() * (volatility_standardize ** 0.5)

        # Sharpe
        sharpe_window = self.__returns.rolling(window=volatility_window).apply(
                                                lambda r: r.mean() / r.std() if r.std() != 0 else 0)
        sharpe_window = sharpe_window.dropna()

        return vol_window, sharpe_window


    def drawdown_series(self):
        cum_returns = (1 + self.__returns).cumprod()
        max_returns = cum_returns.cummax()
        drawdown_series = (cum_returns - max_returns) / max_returns

        return drawdown_series


    def liquidity_matrix(self, liquidity_days=21, liquidity_percentage=0.30):
        # Series of last {liquidity_days} days Median multiply by market insensitivity {liquidity_percentage}.
        negotiated = self.__volume.tail(liquidity_days).median() * liquidity_percentage

        # Liquidity Matrix
        matrix = [self.__positions]
        while True:
            next_colum = matrix[-1] - negotiated
            next_colum = next_colum.clip(lower=0)
            if next_colum.sum() == 0:
                break
            # Create the Matrix
            matrix.append(next_colum)

        # Transform the matrix in DataFrame
        liq_matrix = pd.concat(matrix, axis=1)

        # Create line Liquidated
        sum_label = liq_matrix.sum()
        liq_label = pd.Series(1 - (sum_label / sum_label[0]), name="Liquidated")
        liq_label = pd.DataFrame([liq_label])

        # Add new line
        liq_matrix = pd.concat([liq_label, liq_matrix])

        return liq_matrix


    def VaR_p(self, returns_window=None, days_to_var=252, var_confidence_level = 0.95):
        if returns_window is None:
            returns_window = self.__all_returns_tickers.tail(days_to_var)

        # Covariance Matrix & Std Deviation
        cov_matrix = returns_window.cov()
        portfolio_std = (self.__weights.T @ cov_matrix @ self.__weights) ** 0.5

        # Normal Distribution
        z_score = norm.ppf(1 - var_confidence_level)
        #-loss_area = norm.pdf(z_score)

        # Calculate VaR & CVaR
        VaR = abs(portfolio_std * z_score)
        #-CVaR = abs(portfolio_std * loss_area / (1 - var_confidence_level))

        return VaR #-, CVaR


    def rolling_VaR_p(self, days_to_var=252, var_confidence_level = 0.95):
        VaR_serie = []

        # Mobile window
        for i in range(days_to_var, 1+len(self.__all_returns_tickers)):
            window = self.__all_returns_tickers.iloc[i - days_to_var : i]
            var = self.VaR_p(returns_window=window, days_to_var=days_to_var, var_confidence_level=var_confidence_level)

            # Add to serie
            VaR_serie.append(var)

        # Convert to DataFrame
        var_index = self.__all_returns_tickers.index[days_to_var-1 :]
        var_serie = pd.DataFrame({f"VaR daily % (parametrical {var_confidence_level*100}% confidence)": VaR_serie}, index=var_index)

        return var_serie


    def beta_rolling(self, benchmark='^BVSP', days_to_beta=252):

        data_benchmark = yf.download(benchmark, start=self.__start, end=self.__end, auto_adjust=False)['Adj Close']
        returns_benchmark = data_benchmark.pct_change().fillna(0)
        data = pd.concat([returns_benchmark, self.__all_returns], axis=1)

        # Beta Rolling
        cov = data.iloc[:, 0].rolling(days_to_beta).cov(data.iloc[:, 1])
        var = data.iloc[:, 0].rolling(days_to_beta).var()
        beta_serie = cov / var
        beta_serie = beta_serie.dropna()

        return beta_serie