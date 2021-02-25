import requests 
import nltk
import urllib.request

#nltk.download('punkt')
#nltk.download('stopwords')

# Importo la librería del Rank Tracker
from bs4 import BeautifulSoup
from bs4.element import Comment
from inscriptis import get_text
from urllib.request import urlopen, Request


class headings(): 
    """
    Clase encargada... 
    """
    titulo = ""
    descripcion = ""
    url = ""
    error = ""
    text = ""
    xgrams  = ""

    def __init__(self, URL): 
        self.url = URL
        self.headings = []
        headers =  {"user-agent" : 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'}
        resp = requests.get(URL, headers = headers)
        html = resp.content

        if resp.status_code == 200: 
            soup = BeautifulSoup(html, "html.parser")
            self.titulo = soup.title.text
            if soup.find("meta", property="description"):
                self.descripcion = soup.find("meta", property="description").get('content')
            elif soup.find("meta", property="og:description"):
                self.descripcion = soup.find("meta", property="og:description").get('content')
            elif soup.find("meta", property="twitter:description"):
                self.descripcion = soup.find("meta", property="twitter:description").get('content')

            headers = soup.find_all(["h1", "h2", "h3", "h4"])

            for x in headers:
                h = str(x.name)
                self.headings.append("  "*(int(h[-1])-1) + h + " - " +  x.getText().strip())

            #text_tokens = nltk.tokenize.word_tokenize(soup.get_text())  
            # Recupero el texto para posterior analisis PLN, debería integarlo con soap, pero paso de complicaciones...
            
            headers =  {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
            req = Request(url=URL, headers=headers) 
            html = urllib.request.urlopen(req).read().decode('utf-8')
            self.text = get_text(html)          

            '''
            #Limpiamos el texto de signos de puntuación
            def non_words(content):
                from string import punctuation
                non_words = list(punctuation)
                non_words.extend(map(str, range(10)))
                non_words.extend([u'¿',u'¡'])
                content_words = ''.join([c for c in content if c not in non_words])
                return content_words
            
            clean_text = non_words(text)
            
            import nltk
            from nltk import word_tokenize
            from nltk.text import Text
            from nltk.text import FreqDist
            
            tokens = nltk.word_tokenize(clean_text)
            
            # buscar sinonimos
            
            #print(texto.similar("claustrofobia"))

            #Texto anterior y posterior
            #print(texto.concordance("claustrofobia"))

            #contexto
            #print(texto.common_contexts(["claustrofobia"]))

            #dispersión de palabras
            #texto.dispersion_plot(["claustrofobia", "fobia"])

            #print(len(texto))
            #print(sorted(set(texto))) #ordenado alfabeticamente distinguiendo mayusculas de minusculas

            
            #términos únicos y diversidad léxica
            print(len(set(texto)))
            print(len(set(texto))/len(texto))
            #cuantas veces aparece %
            print(str(texto.count("claustrofobia")) + " veces aparece claustrofobia")
            print(100* texto.count("claustrofobia")/len(texto))

            def lexical_diversity(texto):
                return len(set(texto))/len(texto)
            def percentage(count, total):
                return 100 * count/total
            print("Diversidad Lexica")
            print(lexical_diversity(texto))
            print("Porcentaje de Aparición clausto")
            print(percentage(texto.count("claustrofobia"), len(texto)))
            
            #frecuencia de las palabras
            fdist = FreqDist(texto)
            print("Freqdist de nuestro texto")
            print(fdist)
            print("Most common")
            print(fdist.most_common)
            print("cuantas veces se repite claustrofobia")
            print(fdist["claustrofobia"])
            print("que palabra se repite más")
            print(fdist.max)
            
            fdist.plot(50, cumulative=False)
            

            
            from nltk.corpus import stopwords
            import string
            #print(stopwords.words("spanish"))
            tokens = [w.lower() for w in tokens if w.lower() not in stopwords.words('spanish')]
            tokens = [w for w in tokens if w not in string.punctuation]
            punctCombo = [c+"\"" for c in string.punctuation ]+ ["\""+c for c in string.punctuation]
            tokens = [w for w in tokens if w not in punctCombo]
            #print(tokens)
            #print(len(tokens))
            fdist = nltk.FreqDist(tokens)
            #fdist.plot(20, cumulative=False)
            for word, frequency in fdist.most_common(10):
                self.xgrams = self.xgrams + str(word) + " " + str(frequency) + " - "
            from nltk.util import ngrams
            from collections import Counter
            bigrams = ngrams(tokens, 2)
            trigrams = ngrams(tokens, 3)
            fourgrams = ngrams(tokens, 4)
            fivegrams = ngrams(tokens,5)

            self.xgrams += "\nbigrams\n"
            
            print(self.xgrams)
            
            print("bigrams")
            print(Counter(bigrams).most_common(10))
            
            print("trigrams")
            print(Counter(trigrams).most_common(10))
            print("fourgrams")
            print(Counter(fourgrams).most_common(10))
            print("fivegrams")
            print(Counter(fivegrams).most_common(10))
            ''' 
            self.error = "ok"
        else: 
            self.error = "ko"
            print ("Hay un error al procesar la solicitud: ", resp.status_code)

       