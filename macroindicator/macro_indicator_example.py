import matplotlib.pyplot as plt
import pandas as pd

from dataapi import DBConnect, FocusFeeder
from macroindicator.macro_indicator import macro_indicator

# Citi suprise index data
surprise_index = pd.read_excel(r'C:/Users/mathe/OneDrive/Documentos/Directory R/Citi CES Brazil.xlsx',
                               index_col=0, parse_dates=['Dates'], skiprow=[0, 1, 2, 3, 4])
surprise_index = surprise_index.reindex(index=surprise_index.index[::-1])

# ipca focus data
db_connect = DBConnect('fhreadonly', 'finquant')
ff = FocusFeeder(db_connect)
df = ff.fetch('IPCA', 'yearly')
ff = FocusFeeder(db_connect)
ipca_focus = ff.years_ahead('IPCA', 1)

# obtaining the signals up and down
up_down_df = macro_indicator([surprise_index, ipca_focus])

# function to grab data from bcb
def consulta_bc(codigo_bcb):
  url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
  df = pd.read_json(url)
  df['data'] = pd.to_datetime(df['data'], dayfirst=True)
  df.set_index('data', inplace=True)
  return df

# ipca data
ipca = consulta_bc(433)

# plotting a graph comparing the signals and the real ipca's data
plt.style.use('seaborn')
plt.plot(ipca.index, ipca[ipca.columns[0]].values, color='red', label='IPCA')
plt.legend()
plt.show()


