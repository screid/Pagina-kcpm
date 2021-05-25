import tweepy
import csv
import unicodedata
import os
from datetime import datetime


#Funcion que se usa para limpiar la cadena
def limpiar_cadena(palabra):
    s1 = palabra.replace("ñ", "nn").replace("Ñ", "NN")
    s2 = unicodedata.normalize("NFKD", s1).encode("ascii","ignore").decode("ascii")
    s2 = s2.replace("nn", "ñ"). replace("NN", "Ñ")
    return s2

#Funcion utilizada para rescatar ultimo tweet agregado al documento. (Parametro utilizado mas adelante)
def ultimo_tweet(frase):
    with open('./Tweets/'+frase+'.csv', 'r') as archivo:
        for tweet in reversed(list(csv.reader(archivo))):
            if len(tweet) == 0 :
                continue
            if tweet[0] == 'tweet_id': return 1217444742797123584
            return int(tweet[0])

#Funcion encargada de pedir resultados a la api de tweeter a traves de tweepy.Cursor
def resultados(api, query, modo, ultima_id):
    if ultima_id != 0:
        results = [status for status in tweepy.Cursor(api.search, q= query, lang = 'en', tweet_mode=modo, max_id=ultima_id-1).items(500)]
        return results
    else:
        results = [status for status in tweepy.Cursor(api.search, q=query, lang = 'en', tweet_mode=modo).items(500)]
        return results

#Funcion en la cual se reciben los tweets de la funcion anterior y se rescatan los datos importantes
#en un archivo con el nobre del hashtag y extension csv
def obtener_tweets(consumer_key, consumer_secret, access_token, access_token_secret, ultima_id,frase):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    query = '#'+frase
    with open('./Tweets/'+frase+'.csv', 'a', newline = '') as archivo:
        escribir = csv.writer(archivo)   
        results = resultados(api, query, 'extended', ultima_id)
        print(frase)
        print(hashtag)
        print(hashtags)
        if len(results) == 0: 
            hashtags.remove(frase)
            return
        for tweet in results:
            datos = [
                tweet.id,
                tweet.created_at,
                limpiar_cadena(tweet.full_text.replace('\n',' ').replace(',','.')),
                tweet.favorite_count,
                tweet.retweet_count,
                tweet.user.id,
                tweet.user.screen_name.replace('\n',' ').replace(',','.'),
                limpiar_cadena(tweet.user.location.replace('\n',' ').replace(',','.')),
                tweet.user.followers_count
                ]
            if (tweet.coordinates != None): 
                datos.append(tweet.coordinates['coordinates'][0])
                datos.append(tweet.coordinates['coordinates'][1])
            else :
                datos.append('None')
                datos.append('None')
            try:
                datos.append(tweet.retweeted_status.id)
            except :
                datos.append('N/A')
            escribir.writerow(datos)
            
#Credenciales necesearias para utilizar la API de tweeter
#Obtener credenciales de tweeter y reemplazar valores
consumer_key="API-CONSUMER-KEY"
consumer_secret="API-CONSUMER-SECRET"
access_token="API-ACCESS-TOKEN"
access_token_secret="API-ACCESS-SECRET"

#Funcion en la que se tienen todos los hashtags a buscar que corre de manera permanente hasta que se dejen de 
#recibir tweets, dentro de esta funcion tambien se crean los archivos que no existen y son necesarios.
if __name__ == '__main__':   
    inicio = datetime.now()
    hashtags = ['malware','forkbomb','troyan','backdoortroyan','keyloggers','spyware','adware','exploitcode','jokeprograms','ransomware','hacker','cracker','blackhat','whitehat','grayhat','downloader','sonar','banker','haxdoor','bootkit','browserhijack','crimeware','denialofservice','dos','ddos','socialengineering','wipers','bots','payload','pointofsale','pod','carding','phishing','maliciouscryptominers','maliciousmobilecode','webcrawlers','bootsectorvirus','directactionvirus','residentvirus','multipartitevirus','polymorphicvirus','overwritevirus','spacefillervirus','botnet','codeinjection','sqlinjection','cryptolocker','macrovirus','trickbot']
    for hashtag in hashtags:
        path = './Tweets/'+hashtag+'.csv'
        if os.path.exists(path) :
            os.remove('./Tweets/'+hashtag+'.csv')
    while hashtags:
        for hashtag in hashtags:
            path = './Tweets/'+hashtag+'.csv'
            if not ( os.path.exists(path) ):
                with open('./Tweets/'+hashtag+'.csv', 'w', newline='') as archivo:
                    escribir = csv.writer(archivo)
                    escribir.writerow(['tweet_id','fecha_creacion', 'texto', 'cantidad_likes', 'cantidad_retweet', 'usuario', 'nombre_pantalla', 'ubicacion', 'seguidores','longitud','latitud','id_tweet_original'])
                obtener_tweets(consumer_key, consumer_secret, access_token, access_token_secret, 0,hashtag)
            else:
                ultima_id = ultimo_tweet(hashtag)
                obtener_tweets(consumer_key, consumer_secret, access_token, access_token_secret, ultima_id,hashtag)

    print("Tiempo:", datetime.now() - inicio)