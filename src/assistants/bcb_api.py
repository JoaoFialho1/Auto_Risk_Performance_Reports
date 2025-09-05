import pandas as pd
from datetime import datetime


def BCBdata(start, codigo_serie=12, benchmark_name="CDI (a.d.)"):

    times = datetime.strptime(start, "%Y-%m-%d")
    times = times.strftime("%d/%m/%Y")

    try:
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={times}'
        data = pd.read_json(url)

        # Convert the first column to data (datetime format)
        data = data.rename(columns={"data": "Date", "valor": f"{benchmark_name}"})
        data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
        data.set_index('Date', inplace=True)
        return data

    except Exception as e:
        print("Error, can't download BCB datas. Error:", e)
        return None