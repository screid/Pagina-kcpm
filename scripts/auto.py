import os
from datetime import datetime


inicio = datetime.now()

os.system("python ObtenerTweets.py") 
os.system("python combinar.py")
os.system("python limpiarTweets.py")
os.system("python stemTweets.py")
os.system("python weight.py")
os.system("python k_cpm.py")
os.system("python Insert_Tweets_Limpios.py")
os.system("python Insertar_DB.py")
#os.system("python Insertar_RT.py") #No se puede correr por falta de geocoder (google api)
os.system("python GenerarMapaInicial.py")

print("Tiempo TOTAL:", datetime.now() - inicio)
