from datetime import datetime
import json
import random
import haravasto as hr
import ikkunasto as ik
import tulva as tu

tila = {
    "kentta": [],
    "jaljella": [],
    "lippu": [],
    "leveys": 0,
    "korkeus": 0,
    "miinoja": 0,
    "lopetus": " ",
    "aloitus_aika": 0,
    "lopetus_aika": 0,
    "siirto":0,
    "aika": 0.0
     
}
peli = {"nro": 0,
            "aika": 0,
            "kesto": 0,
            "siirrot": 0,
            "tulos": 0,
            "kentan_koko": 0,
            "miinat":0
            }

tulokset = {"kokoelma": [peli]
           }
def lataa_tulokset(tiedosto="tulokset.txt"):
    """ladataan aiemmat pelitilastot tiedostosta"""
    try:
        with open(tiedosto) as lahde:
            tulokset["kokoelma"] = json.load(lahde)
    except (IOError, json.JSONDecodeError):
        print("Tiedoston avaaminen ei onnistunut. Aloitetaan tyhjällä kokoelmalla")

    
    
def miinakentta_alustus():
    """Luodaan miinakenttä ja miinoitetaan se"""
    global leveys, korkeus, miinoja, tekstilaatikko, kentta, avaus

    tila["lopetus"] = " "
    tila["lippu"] = []
    siirto = 0
    tila["siirto"] = siirto
    aloitus_aika = int(datetime.now().strftime("%M"))
    aika = datetime.now().strftime("%c")
    peli["aika"] = aika
    tila["aloitus_aika"] = aloitus_aika
    nro = tulokset["kokoelma"][-1]["nro"]
    if nro is False:
        nro = 0
    
    nro = nro + 1 
    peli["nro"] = nro
    l = ik.lue_kentan_sisalto(leveys)
    k = ik.lue_kentan_sisalto(korkeus)
    m = ik.lue_kentan_sisalto(miinoja)
    
    tila["leveys"] = l
    tila["korkeus"] = k
    tila["miinoja"] = m

    try:
        l = int(l)
        k = int(k)
        m = int(m)
     
        if m > k*l:
            virhetila = "Korjaa"
            viesti = "Kenttää ei voida luoda, liikaa miinoja"
            lisays = " "
            nayta_viesti(virhetila, viesti, lisays)
        
        if l and k and m and m <= k*l:
            #tarkistetaan kentän koko ja miinojen määrä
            peli_tila = "Peli voi alkaa"
            viesti = "Miinakenttä luotu! \nkentän koko {} x {} \
            \nkentälle on piilotettu {} miinaa".format(l, k, m)
            lisays = "Pidä hauskaa"

            #rakennetaan kentta
            kentta = []
            for rivi in range(k):
                kentta.append([])
                for sarake in range(l):
                    kentta[-1].append(" ")
            tila["kentta"] = kentta

            #muodostetaan vapaat koordinaatit
            jaljella = []
            for x in range(l):
                for y in range(k):
                    jaljella.append((x, y))
                    tila["jaljella"] = jaljella

            #kentän miinoitus
            miinoita(kentta, jaljella, m)
            
            #ik.avaa_viesti_ikkuna("Peli alkaa", viesti)
            nayta_viesti(peli_tila, viesti, lisays)
            peli_ikkuna()
            
    except ValueError:
        virhetila = "Korjaa!"
        viesti = "Korjaa tiedot"
        lisays = " "
        nayta_viesti(virhetila, viesti, lisays)
        
    
def peli_ikkuna():
    kentan_piirto()
    
    
def kasittele_hiiri(x, y, nappi, muokkausnapit):
    """Tämä ohjaa eteenpäin kun hiiren painiketta I tai II on painettu"""
    
    kentta = tila["kentta"]
    siirto = tila["siirto"]
    if nappi == 1:
        siirto = siirto + 1
        tila["siirto"] = siirto
        tarkistus(kentta, x, y)
        
    elif nappi == 2:
        siirto = siirto + 1
        tila["siirto"] = siirto
        aseta_lippu(kentta, x, y)
    

def piirra_peli():
    """Tällä piirretään uusi tilanne kentällä"""
    
    hr.tyhjaa_ikkuna()
    hr.piirra_tausta()
    kentta = tila["kentta"]
    lopetus = tila["lopetus"]
    lippu = tila["lippu"]
    k = len(kentta)
    l = len(kentta[0])
    
    #piirretään kenttä
    hr.aloita_ruutujen_piirto()
    for i in range(len(kentta)):
        rivi = kentta[i]      
        for j in range(len(rivi)):
            merkki = rivi[j]
            if merkki == "x" and lopetus == " ":
                merkki = " "
    
            for p in range(len(lippu)):
                if (j,i) == lippu[p]:
                    merkki = "f"
                     
            hr.lisaa_piirrettava_ruutu(merkki, 40*j, ((k-1)*40 - 40*i))

    hr.piirra_ruudut()

   
def kentan_piirto():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
        
    l = int(tila["leveys"])
    k = int(tila["korkeus"])
    m = int(tila["miinoja"])
    
    hr.lataa_kuvat("spritet")
    hr.luo_ikkuna(40*l, 40*k)
    hr.aseta_piirto_kasittelija(piirra_peli)
    hr.aseta_hiiri_kasittelija(kasittele_hiiri)
    hr.aloita()
    

def miinoita(kentta, jaljella, n):
    """Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin. paikat arvotaan jäljellä olevista
    koordinaateista """
            
    for i in range(n):
        (mx, my) = random.choice(jaljella)
        kentta[my][mx] = "x"
        jaljella.remove((mx, my))
    
    


def tarkistus(kentta, x, y):
   
    o = 0
    lippu = tila["lippu"]
    k = len(kentta) - 1
    l = len(kentta[0])
    x1 = round((x-20) / 40)
    y1 = k - round((y - 20) / 40)
            
    if kentta[y1][x1] == "x":
        tila["lopetus"] = "Osuit miinaan"
        lopetus()
        
    elif kentta[y1][x1] == " ":
        print("tyhjä")
        tu.tulvataytto(kentta, x1, y1)
        for i in range(len(kentta)):
            rivi = kentta[i]
            p = rivi.count(" ")
            o = o + p
            
        if o == 0:
            tila["lopetus"] = "Hienoa. Avasit kaikki vapaat ruudut"
            lopetus()
   
    piirra_peli()
        
        
def aseta_lippu(kentta, x, y):
    """Asetetaan lippu kentälle"""
   
    lippu = tila["lippu"]
    k = len(kentta) - 1
    l = len(kentta[0])
    x1 = round((x - 20) / 40)
    y1 = k - round((y - 20) / 40)

    if kentta[y1][x1] == " " or kentta[y1][x1] == "x":
        lippu.append((x1, y1))
    
        
def aloitus():
    """Pelin alustaminen ja kyselyruudun luominen"""

    global leveys, korkeus, miinoja, tekstilaatikko
    leveys = tila["leveys"]
    korkeus = tila["korkeus"]
    miinoja = tila["miinoja"]
    lippu = tila["lippu"]
    lataa_tulokset() #funktio joka avaa tiedoston jossa tulos tilastot
    kysely_ikkuna = ik.luo_ikkuna("Miinakentän koko")

    #kehykset
    viite_kehys = ik.luo_kehys(kysely_ikkuna, ik.VASEN)
    syote_kehys = ik.luo_kehys(kysely_ikkuna, ik.VASEN)
    nappi_kehys = ik.luo_kehys(kysely_ikkuna, ik.VASEN)
    ala_kehys = ik.luo_kehys(kysely_ikkuna, ik.ALA)
    
   
    #arvojen syöttäminen  
    leveys_ohje = ik.luo_tekstirivi(viite_kehys, "Kentän leveys: ")
    leveys = ik.luo_tekstikentta(syote_kehys)
    korkeus_ohje = ik.luo_tekstirivi(viite_kehys, "Kentän korkeus: ")
    korkeus = ik.luo_tekstikentta(syote_kehys)
    miina_ohje = ik.luo_tekstirivi(viite_kehys, "Miinojen määrä: ")
    miinoja = ik.luo_tekstikentta(syote_kehys)

    #tekstilaatikko mahdolliseen tulostukseen
    tekstilaatikko = ik.luo_tekstilaatikko(ala_kehys, 30, 5)

    l = ik.lue_kentan_sisalto(leveys)
    k = ik.lue_kentan_sisalto(korkeus)
    m = ik.lue_kentan_sisalto(miinoja)
   
    aloita_nappi = ik.luo_nappi(nappi_kehys, "Aloita", miinakentta_alustus)
    lopeta_nappi = ik.luo_nappi(nappi_kehys, "Lopeta", lopeta)
    tilasto_nappi = ik.luo_nappi(nappi_kehys, "Tilastot", tulostus)
    ik.kaynnista()

def nayta_viesti(virhetila, viesti, lisays = "Sulje kenttä aloittaaksesi \
uuden pelin"):

    
    ik.avaa_viesti_ikkuna(virhetila, viesti+"\n"+lisays)


def tilasto():
    
    aloitus_aika = tila["aloitus_aika"]
    lopetus_aika = tila["lopetus_aika"]
    kesto = int(tila["lopetus_aika"]) - int(tila["aloitus_aika"])
    peli["kesto"] = kesto 
    peli["siirrot"] = tila["siirto"]
    peli["tulos"] = tila["lopetus"]
    peli["kentan_koko"] = [tila["leveys"], tila["korkeus"]]
    peli["miinat"] = tila["miinoja"]
    
    tallenna_kokoelma()

def tulostus():
    "tässä kirjoitetaan tilastot ikkunaan ja tallennetaan tiedostoon tulokset"""
    for i in tulokset:
        nro = peli["nro"]
        aika = peli["aika"]
        kesto = peli["kesto"]
        siirrot = peli["siirrot"]
        tulos = peli["tulos"]
        kentta = peli["kentan_koko"]
        miinat = peli["miinat"]
        viesti = "pelin nro: {} \naloitus aika: {} \npelin kesto (min): {} \nsiirrot: {} \ntulos: {} \nkentän koko: {} \nmiinoja: {}".format(nro, aika, kesto, siirrot, tulos, kentta, miinat)
        ik.kirjoita_tekstilaatikkoon(tekstilaatikko, viesti)
    
    
    
def tallenna_kokoelma(tiedosto="tulokset.txt"):
    """tallennetaan luotu peli["kokoelma"] tiedostoon tulokset.txt"""
    try:
        with open(tiedosto, "a") as kohde:
            json.dump(tulokset["kokoelma"], kohde)
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui")

    
def lopetus():
    """Pelin lopetus"""

    lippu = tila["lippu"]
    for i in range(len(kentta)):
        rivi = kentta[i]
        for j in range(len(rivi)):
            tu.tulvataytto(kentta, j, i)       

    lippu.clear()
    tila["lippu"] = lippu
    piirra_peli()
    nayta_viesti(tila["lopetus"], tila["lopetus"])
    lopetus_aika = int(datetime.now().strftime("%M"))
    tila["lopetus_aika"] = lopetus_aika
    tilasto()
    
    
def lopeta():
    
    ik.lopeta()
    quit()
    
if __name__ == "__main__":
    
    try:
        aloitus()
    except KeyboardInterrupt:
        print("Ohjelma keskeytettiin, kokoelmaa ei tallennettu")

