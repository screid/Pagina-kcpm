from datetime import datetime
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from networkx.algorithms.community import k_clique_communities
import csv

inicio = datetime.now()

discriminacion_tdif = 0.25

documento_stemming = list()
with open("tweetsStemming.csv", 'r') as f:
    contenido = csv.reader(f)
    for tweet in contenido:
        if tweet[2] == 'texto': continue
        documento_stemming.append(tweet[2].strip())
        
#Vector Tdif
vectorizer = TfidfVectorizer(smooth_idf=False)
#Se le aplica Tdif al documento que se le hizo stemmming
vectors = vectorizer.fit_transform(documento_stemming) #.toarray()
tdif_array = vectorizer.get_feature_names()


tdif_final =list()
for vector in vectors:
    vector = vector.toarray()[0]
    vector_temp = list()
    for index, data in enumerate(vector):
        if (data > discriminacion_tdif):
            vector_temp.append(tdif_array[index])
    vector_temp = ' '.join(vector_temp)
    tdif_final.append(vector_temp)

vector_no_stopwords = CountVectorizer()
T_no_stopwords = vector_no_stopwords.fit_transform(tdif_final)
words_tags_no_stopwords = vector_no_stopwords.get_feature_names()

count_model = CountVectorizer(ngram_range=(1,1))
X = count_model.fit_transform(tdif_final)

Xc = (X.T * X)
Xc.setdiag(0)

words_cooccurrence = count_model.get_feature_names()

matrix_cooccurrence = Xc #.toarray()

tdif_lista = list()
for palabra in words_cooccurrence:
    tdif_lista.append(palabra)
    
matrix_final = list()

for i, vector_cooccurrence in enumerate(matrix_cooccurrence):
    vector_cooccurrence = vector_cooccurrence.toarray()[0]
    for j, cooccurrence in enumerate(vector_cooccurrence):
        if(j > i and cooccurrence > 0):
            cooccurrence_temp_vector = list()
            cooccurrence_temp_vector.append(tdif_lista[i])
            cooccurrence_temp_vector.append(tdif_lista[j])
            cooccurrence_temp_vector.append(cooccurrence)
            matrix_final.append(cooccurrence_temp_vector)
        
maximo = 0
for m in matrix_final:
    if m[2] > maximo: maximo = m[2]

with open('weight_file.txt', 'w') as archivo:
    for i in range(len(matrix_final)):
        matrix_final[i][2] = float(matrix_final[i][2])/float(maximo)
        archivo.write(str(matrix_final[i][0]) + " " + str(matrix_final[i][1]) + " " + str(matrix_final[i][2]) + "\n")

with open("words.txt","w") as archivo:
    for i in tdif_array:
        archivo.write(i + '\n')

print ("Tiempo:", datetime.now() - inicio)