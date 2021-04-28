import pandas as pd
import mysql.connector
from datetime import datetime

inicio = datetime.now()

try:
    #conn = psycopg2.connect(database_connection)
    conn = mysql.connector.connect(host='localhost',
                                   database='cyberaware',
                                   user='root',
                                   password='Unab.2019')
 
except:
    print("No pude conectarme a la base de datos")
cur = conn.cursor()

cur.execute("""DELETE FROM tweets""")

document = list()

data = pd.read_csv('tweetsLimpios.csv')
a = data['tweet_id'].tolist()
c = data['texto'].tolist()

for linea in c:
    document.append(linea)

for index,tweet in enumerate(document):
    cur.execute("""INSERT INTO tweets(tweet_id,texto) 
                VALUES(%s,'%s') """ % 
                (a[index],tweet))
    conn.commit()
    
print("Tiempo:", datetime.now() - inicio)