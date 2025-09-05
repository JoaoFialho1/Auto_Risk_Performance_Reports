import pandas as pd

def read(data, sheet_name="Planilha1"):
    df = pd.read_excel(data, sheet_name=sheet_name)

    # Tickers & Weights
    tickers = df.iloc[:,0].tolist()
    weights = df.iloc[:,1].astype(float).tolist()

    return tickers, weights