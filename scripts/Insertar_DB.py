import numpy as np
import nltk
import pandas as pd
from scipy.spatial.distance import cosine
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import mysql.connector

np.set_printoptions(threshold=1)
#database_connection = "dbname='cpm_dev' user='postgres' password='Unab2020' host='localhost' "

#Funcion utilizada insertar tweets en la base de datos y crear un vector tfidf
def documentVectorize():

    document = list()

    data = pd.read_csv('tweetsStemming.csv')
    a = data['tweet_id'].tolist()
    b = data['fecha_creacion'].tolist()
    c = data['texto'].tolist()
    d = data['cantidad_likes'].tolist()
    e = data['cantidad_retweet'].tolist()
    f = data['usuario'].tolist()
    g = data['nombre_pantalla'].tolist()
    h = data['ubicacion'].tolist()
    i = data['seguidores'].tolist()
    j = data['id_tweet_original'].tolist()
    for linea in c:
        document.append(linea)
    
    for index,tweet in enumerate(document):
        if str(j[index]) == 'nan': j[index] = 'NULL'
        cur.execute("""INSERT INTO stemming(id,tweet_id,fecha_creacion,texto,cantidad_likes,cantidad_rt,id_usuario,nombre_usuario,ubicacion,cantidad_seguidores,id_tweet_original,created_at,updated_at) 
                    VALUES(%s,%s,'%s','%s',%s,%s,%s,'%s','%s',%s,%s,now(),now()) """ % 
                    (index,a[index],b[index],tweet,d[index],e[index],f[index],g[index],h[index],i[index],j[index]))
        conn.commit()

    vectorizer = TfidfVectorizer(smooth_idf=False)
    vectors = vectorizer.fit_transform(document)#.toarray()
    return vectors



startTime = datetime.now()

document = list()
wordsArray = list()

#Se leen los archivos creados anteriormente y se guardan en sus respectivos arreglos
with open('words.txt','r') as archivo:
    for linea in archivo.readlines():
        linea = linea.splitlines()
        linea = linea[0]
        wordsArray.append(linea)

with open('k_cpm/cpm_cluster_K11.txt', 'r') as archivo:
    for linea in archivo.readlines():
        if linea[0] != '\n' and linea[0] != '#':
            linea = linea.splitlines()
            linea = linea[0].split()
            document.append(linea)

#Se conecta a la base de datos
try:
    #conn = psycopg2.connect(database_connection)
    conn = mysql.connector.connect(host='localhost',
                                   database='cyberaware',
                                   user='root',
                                   password='Unab.2019')
 
except:
    print("No pude conectarme a la base de datos")
cur = conn.cursor()

#se borra el contido de la base de datos para no duplicar tweets en caso de que estos ya existan
cur.execute("""DELETE FROM rel_stemming_comunidades""")
cur.execute("""DELETE FROM comunidades""")
cur.execute("""DELETE FROM stemming""")

conn.commit()

#Se insertan las comunidades en la base de datos
for linea in document:
    linea = ' '.join(linea)
    cur.execute("""INSERT INTO comunidades(nombre_comunidades, texto_comunidades, created_at, updated_at) 
                   VALUES('nombre','%s', now(), now() );""" % linea)
conn.commit()

comunidades = list()

cur.execute("SELECT texto_comunidades, id FROM comunidades")
filas = cur.fetchall()
filas = np.asarray(filas)

comunidades.append([' '.join(wordsArray),0])

for fila in filas:
    #Se agrega a la lista comunidades la comunidad y su ID
    comunidades.append([fila[0],fila[1]])

result = list()

for mt in comunidades:
    result.append(mt[0])

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(result).toarray() #Quizas lo saque

#Se remueve el vector de palabras una vez generado el vector
matrixComunidades = vectors[1:]

comunidades = comunidades[1:]

documentMatrix = documentVectorize()

print ("Starting insert relationship between communities and documents ...")
#Se calcula e inserta en la base de datos la relacion que existe entre cada tweet y cada comunidad 
matrixRelationDocumentCommunity = list()
a  = 0
for index, ini in enumerate(documentMatrix):
    ini = ini.toarray()[0]
    minor = [1,0,index]
    for indexComunidad, comu in enumerate(matrixComunidades):
        distancia = cosine(ini,comu)
        try:
            cur.execute("INSERT INTO rel_stemming_comunidades(grado, comunidades_id, stemming_id, created_at, updated_at) VALUES(%s,%s,%s,now(),now());" %
            ((float("{0:.3f}".format((1-distancia)))*100),comunidades[indexComunidad][1],index))
            conn.commit()
        except:
            a+=1
            print (distancia)
            continue
            
    matrixRelationDocumentCommunity.append(minor)

print ("Tiempo: {}".format(datetime.now() - startTime))

