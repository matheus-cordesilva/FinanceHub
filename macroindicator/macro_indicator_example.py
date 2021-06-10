import matplotlib.pyplot as plt
import pandas as pd
import os

from dataapi import DBConnect, FocusFeeder
from datasets.datasets_base_io import datasets_path_name
from macroindicator.macro_indicator import macro_indicator

# Citi suprise index data
path = datasets_path_name()
surprise_index = pd.read_excel(r'' + str(path) + '\Citi CES Brazil.xlsx',
                               index_col=0, parse_dates=['Dates'], skiprows=[0, 1, 2, 3, 4])
surprise_index = surprise_index.reindex(index=surprise_index.index[::-1])

# ipca focus data
db_connect = DBConnect('fhreadonly', 'finquant')
ff = FocusFeeder(db_connect)
df = ff.fetch('IPCA', 'yearly')
ff = FocusFeeder(db_connect)
ipca_focus = ff.years_ahead('IPCA', 1)

# obtaining the signals up and down
up_down_df = macro_indicator([surprise_index, ipca_focus])
# up_down_df.to_csv('up_down.csv')
print(up_down_df)


