
# Archivo de arranque del programa. Desde aquí podrás configurarlo. 
from searchEngine.google import GoogleSearch
from headings.headings import headings


# Importamos la libreria SYS y otras
import sys 
import io
import os
import nltk

#Necesarios la primera vez
nltk.download('punkt') 
nltk.download('stopwords')

#Recupero resultados en google para la keyword
keywords = "claustrophobia"
idioma = "en"

texto0 = ""
textoheadings = ""

urls = GoogleSearch(keywords, idioma, True)
if urls.error == "ko":
     #print("Mierda...Error... no lo he definido...")
     exit()


#uso un directorio para guardar los ficheros de resultados. Si no existe lo creo
directorio = "Ficheros"
try:
  os.stat(directorio)
except:
  #print("Unexpected error:", sys.exc_info()[0])
  os.mkdir(directorio)

#recupero artículos luego ya trabajaré con ellos
articulos = []
i= 0
palabras = 0
for x in urls.listaUrls:
    i+=1
    hola = headings(x)
    articulos.append(hola)
    print(i)
    if i < 6: 
      texto0 += hola.text
      #print(len(texto0))
     
    if hola.error == "ko":
        print("Error xxx")
        continue
    for h in hola.headings:
        textoheadings += h + " "
     
#print( str(palabras/5), " media de palabras en los 5 primeros artículos" )

def analisisPln(texto, titulo):

  #Limpiamos el texto de signos de puntuación
  def non_words(content):
      from string import punctuation
      non_words = list(punctuation)
      non_words.extend(map(str, range(10)))
      non_words.extend([u'¿',u'¡'])
      content_words = ''.join([c for c in content if c not in non_words])
      return content_words

  clean_text = non_words(texto)

  import nltk
  from nltk import word_tokenize
  from nltk.text import Text
  from nltk.text import FreqDist

  tokens = nltk.word_tokenize(clean_text)

  from nltk.corpus import stopwords
  import string
  idiomaStop = "spanish"
  if idioma == "en":
    idiomaStop = "english"
  
  tokens = [w.lower() for w in tokens if w.lower() not in stopwords.words(idiomaStop)]
  tokens = [w for w in tokens if w not in string.punctuation]
  punctCombo = [c+"\"" for c in string.punctuation ]+ ["\""+c for c in string.punctuation]
  tokens = [w for w in tokens if w not in punctCombo]
  fdist = nltk.FreqDist(tokens)
  xgrams = ""
  for word, frequency in fdist.most_common(30):
      xgrams = xgrams + str(word) + " " + str(frequency) + " - "
  from nltk.util import ngrams
  from collections import Counter
  bigrams = ngrams(tokens, 2)
  trigrams = ngrams(tokens, 3)
  #fourgrams = ngrams(tokens, 4)
  #fivegrams = ngrams(tokens,5)
  analisis = ""
  analisis += "----------------------------------------\n"
  analisis += titulo  + "\n"
  analisis += "Palabras más usadas: " + xgrams + "\n"
  analisis += "Agrupaciones de 2 palabras: "
  analisis += ', '.join(map(str, Counter(bigrams).most_common(20)))
  analisis += "\n"
  analisis += "Agrupaciones de 3 palabras: "
  analisis += ', '.join(map(str, Counter(trigrams).most_common(10)))
  analisis += "\n"
  '''
  analisis += "Agrupaciones de 4 palabras"
  analisis += ', '.join(map(str, Counter(fourgrams).most_common(10)))
  analisis += "\n"
  analisis += "Agrupaciones de 5 palabras"
  analisis += ', '.join(map(str, Counter(fivegrams).most_common(10)))
  analisis += "\n"
  '''
  return analisis


#abro fichero para escribir headings
f = open(directorio + "\\" + keywords + ".txt", "w", encoding="utf-8")
#Imprimo las entidades
f.write("Keyword: " + keywords + "  idioma: " + idioma + "\n")
f.write("----------------------------------------\n")
if urls.gmb != "":
  f.write("Local pack:")
  f.write("\n")
  f.write(urls.gmb)
if urls.fragmentoDestacado != "":
  f.write("Fragmento destacado " + str(len(urls.fragmentoDestacado)) + " carácteres: " + urls.fragmentoDestacado + "\n")
f.write("Entidades google imágenes" + urls.entidades  + "\n")
if urls.preguntas != "":
  f.write("Preguntas relacionadas" + urls.preguntas  + "\n")
if urls.busquedas !="":
  f.write("Búsquedas relacionadas" + urls.busquedas + "\n")

#pln headings
#quito hs
hs = ['h1', 'h2', 'h3', 'h4', 'h5']
querywords = textoheadings.split()
resultwords  = [word for word in querywords if word.lower() not in hs]
textoheadings = ' '.join(resultwords)
textoheadings = analisisPln(textoheadings, "Palabras más usadas en los headings de los 10 primeros artículos")
f.write(textoheadings)


#pln texto
texto0 = analisisPln(texto0, "Palabras más usadas en los 5 primeros artículos")
f.write(texto0)
f.write("----------------------------------------\n")
f.write("Resultados búsqueda google\n")
for arti in articulos:
   
    if arti.error == "ko":
        print("Error xxx")
        continue
    f.write(arti.url + "\n")
    f.write("Título: " + arti.titulo + "\n")
    f.write("Descripción: " + arti.descripcion + "\n")
    f.write("Headings: " + "\n")
    for h in arti.headings:
        f.write(h + "\n")
    f.write("\n")  

f.close
print("NO TE OLVIDES DE COMPROBAR LAS SERPS!")