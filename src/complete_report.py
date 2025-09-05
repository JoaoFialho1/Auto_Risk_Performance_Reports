import pandas as pd
from datetime import timedelta
from src.functions import Portfolio
from src.assistants.bcb_api import BCBdata

def general_report(tickers, weights, start, end=None, name="",
           volatility_window=21, volatility_standardize=252,
            liquidity_days=21, liquidity_percentage=0.30,
             days_to_var=252, var_confidence_level = 0.95,
              benchmark_sharpe="^BVSP", days_to_beta=252,
                benchmark_name="CDI (a.d.)",
               portfolio_inicial_value=100000000, bcb_serie_key=12):
    port =  Portfolio(tickers=tickers, weights=weights, start = start, end=end, portfolio_inicial_value=portfolio_inicial_value)

    # Datas
    volatility, sharpe = port.volatility_sharpe(volatility_window=volatility_window, volatility_standardize=volatility_standardize)
    var_serie = port.rolling_VaR_p(days_to_var=days_to_var, var_confidence_level=var_confidence_level)
    beta_serie = port.beta_rolling(benchmark=benchmark_sharpe, days_to_beta=days_to_beta)
    drawndown = port.drawdown_series()
    liquid_matrix = port.liquidity_matrix(liquidity_days=liquidity_days, liquidity_percentage=liquidity_percentage)
    returns_accumulate = port.returns_accumulate
    returns = port._Portfolio__returns
    portfolio_nav = port.portfolio_nav

    # Get CDI datas from BCB
    cdi = BCBdata(start, bcb_serie_key, benchmark_name) * 0.01

    time = cdi.index[0] - timedelta(days=1)
    first_line = pd.Series([0], index=[time], name=benchmark_name)

    # CDI Returns
    cdi_accumulate = (1 + cdi).cumprod() - 1
    cdi_accumulate = pd.concat([first_line, cdi_accumulate])
    cdi_accumulate = cdi_accumulate.rename(columns={benchmark_name: f"{benchmark_name} accumulated"})

    # Portfolio in cdi
    benchmark_nav = (1 + cdi_accumulate) * portfolio_inicial_value
    benchmark_nav = benchmark_nav.rename(columns={f"{benchmark_name} accumulated": "Benchmark NAV"})


    # Export in Files
    series = pd.concat([volatility.rename(f"Vol % (standardize {volatility_standardize} days {volatility_window}d window)"),
                        drawndown.rename("Drawdown %"),
                         var_serie,
                          sharpe.rename(f"Sharpe ({volatility_window}d window)"),
                           beta_serie.rename(f"Beta ({days_to_beta}d window)"),
                            returns_accumulate.rename("Portfolio return cumulative %"),
                             portfolio_nav.rename("Portfolio NAV"),
                               benchmark_nav,
                                cdi,
                                 cdi_accumulate,
                                    returns.rename("Portfolio returns %")],
                                axis=1)

    # Name and diretory
    if name:
        title = f"{name}_"
    else:
        title=""
    series.to_csv(f"outputs/{title}series.csv", index=True, header=True)
    liquid_matrix.to_csv(f"outputs/{title}liquidity_matrix.csv", index=True)