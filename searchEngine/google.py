# Importamos la librería requests 
import requests 
# Importo la librería del Rank Tracker
from bs4 import BeautifulSoup
class GoogleSearch(): 
    """
    Clase encargada... 
    """
    listaUrls = []
    error = ""
    entidades = ""
    preguntas = ""
    busquedas = ""
    fragmentoDestacado = ""
    gmb = ""
    def __init__(self, QUERY, idioma = "es", entidadesImagenes = False): 
        #https://www.google.com/search?hl=de&
        URL = "https://www.google.com/search?hl=%s&q=%s&oq=%s" % (idioma, QUERY, QUERY)
        #print(URL)
        headers =  {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
        resp = requests.get(URL, headers = headers)
        html = resp.content

        if resp.status_code == 200: 
            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("div", {"class" : "g"})
            for x in links:
                a = x.find("a", href = True)
                u = a["href"]
                if str(u).startswith("http"):
                    if "#" not in u:
                        self.listaUrls.append(u)
                    else:
                        self.listaUrls.append(str(u).split("#")[0])
            #print(len(self.listaUrls))

             #busco las preguntas relacionadas si hay
            preguntasRel = soup.find_all("div", {"class" : "related-question-pair"}) 

            for p in preguntasRel:
                u = p.getText()
                self.preguntas += " - " + u
                
            #Busquedas relacionadas
            busquedasRel = soup.find_all("p", {"class" : "nVcaUb"}) 

            for p in busquedasRel:
                u = p.getText()
                self.busquedas += " - " + u

            if self.busquedas == "":
                #Busquedas relacionadas
                busquedasRel = soup.find_all("a", {"class" : "k8XOCe"}) 

                for p in busquedasRel:
                    u = p.getText()
                    self.busquedas += " - " + u
            
            fragmento = soup.find_all("span", {"class" : "hgKElc"}) 

            for p in fragmento:
                u = p.getText()
                self.fragmentoDestacado += u.strip()


            #VkpGBb
            localpack = soup.find_all("div", {"class" : "VkpGBb"}) 

            for p in localpack:
                tx = p.find("div", {"class" : "dbg0pd"})
                self.gmb += "    " + tx.getText()
                a = p.find("a", href = True)
                if a is not None:
                    self.gmb += " - " + a["href"]
                self.gmb += "\n"

            self.error = "ok"
        else: 
            self.error = "ko"
            print ("Hay un error al procesar la solicitud: ", resp.status_code)
        
        if entidadesImagenes == True:
            URL = "https://www.google.com/search?hl=" + idioma + "&q=" + QUERY+ "&source=lnms&tbm=isch"
            resp = requests.get(URL, headers = headers)
            html = resp.content

            if resp.status_code == 200: 
                soup = BeautifulSoup(html, "html.parser")
                #busco enlaces de las serps
                links = soup.find_all("span", {"class" : "hIOe2"}) 
                for a in links:
                    u = a.getText()
                    self.entidades += " - " + u
                    #print(u + " - ")
                self.error = "ok"

            else: 
                self.error = "ko"
                print ("Hay un error al procesar la solicitud: ", resp.status_code)
        