from keplergl import KeplerGl
import pandas as pd
from mapa_bienvenida import config
import os
import shutil

df= pd.read_csv("LocationAPI.csv")
df2= pd.read_csv("LocationArc.csv")
map_1 = KeplerGl()
map_1.add_data(data=df, name='data_1')
map_1.add_data(data=df2, name='data_2')

map_1.save_to_html(data={'data_1': df, 'data_2': df2}, config=config, file_name='mapa_inicial.html', read_only=False)
shutil.copyfile("mapa_inicial.html", "/var/www/html/back/tweets/mapa_inicial.html")
