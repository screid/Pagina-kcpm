import unicodedata
import re
import csv
from datetime import datetime

def limpiar_cadena(palabra):
    palabra = palabra.replace("'",'')
    palabra = re.sub(r'http\S+', '', palabra )
    s1 = palabra.replace("ñ", "nn").replace("Ñ", "NN")
    s2 = unicodedata.normalize("NFKD", s1).encode("ascii","ignore").decode("ascii")
    return s2

#Funcion que elimina caracteres no reconocidos por python
def clean_str(string):
    string = re.sub(r"\'s", "", string)
    string = re.sub(r"\'ve", "", string)
    string = re.sub(r"n\'t", "", string)
    string = re.sub(r"\'re", "", string)
    string = re.sub(r"\'d", "", string)
    string = re.sub(r"\'ll", "", string)
    string = re.sub(r",", "", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", "", string)
    string = re.sub(r"\)", "", string)
    string = re.sub(r"\?", "", string)
    string = re.sub(r"'", "", string)
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"[0-9]\w+|[0-9]","", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(r'http\S+', '', string)
    return string.strip().lower()

inicio = datetime.now()

with open('tweetsLimpios.csv', 'w' , newline='') as archivo:
    csv_writer = csv.writer(archivo)
    with open('combinados.csv', 'r') as combi:
        contenido = combi.readlines()
        for tweet in contenido:
            tweet = tweet.strip()
            tweet = tweet.split(',')
            tweet[2] = limpiar_cadena(tweet[2])
            tweet[2] = clean_str(tweet[2])
            if len(tweet[2]) == 0: print (tweet[0])
            tweet[7] = limpiar_cadena(tweet[7])
            tweet[7] = clean_str(tweet[7])
            csv_writer.writerow(tweet)

print("Tiempo:", datetime.now() - inicio)