import csv
import unicodedata

def limpiar_cadena(palabra):
    s1 = palabra.replace("ñ", "nn").replace("Ñ", "NN")
    s2 = unicodedata.normalize("NFKD", s1).encode("ascii","ignore").decode("ascii")
    return s2

hashtags = ['malware','forkbomb','troyan','backdoortroyan','keyloggers','spyware','adware','exploitcode','jokeprograms','ransomware','hacker','cracker','blackhat','whitehat','grayhat','downloader','sonar','banker','haxdoor','bootkit','browserhijack','crimeware','denialofservice','dos','ddos','socialengineering','wipers','bots','payload','pointofsale','pod','carding','phishing','maliciouscryptominers','maliciousmobilecode','webcrawlers','bootsectorvirus','directactionvirus','residentvirus','multipartitevirus','polymorphicvirus','overwritevirus','spacefillervirus','botnet','codeinjection','sqlinjection','cryptolocker','macrovirus','trickbot']
i = 1
id_unicos = set()
header = ['tweet_id','fecha_creacion','texto','cantidad_likes','cantidad_retweet','usuario','nombre_pantalla','ubicacion','seguidores','longitud','latitud','id_tweet_original']

with open('combinados.csv', 'r', newline='') as archivoCreado:
    linea = 0
    contenido = csv.reader(archivoCreado)
    for tweet in contenido:
        if linea == 0:
            linea += 1
            continue
        id_unicos.add(tweet[0])

with open('combinados.csv', 'a', newline='') as archivoCreado:
    writer = csv.writer(archivoCreado)
    #writer.writerow(header)
    for h in hashtags:
        with open('Tweets/' + h + '.csv', 'r') as archivo:
            n_linea = 0
            contenido = archivo.readlines()
            for linea in contenido:
                if n_linea == 0:
                    n_linea += 1
                    continue
                else:
                    linea = linea.split(',')
                    if linea[0] not in id_unicos and len(linea) == 12:
                        linea[2] = limpiar_cadena(linea[2])
                        linea[7] = limpiar_cadena(linea[7])
                        linea[6] = limpiar_cadena(linea[6])
                        linea[-1] = linea[-1].strip()
                        id_unicos.add(linea[0])
                        writer.writerow(linea)