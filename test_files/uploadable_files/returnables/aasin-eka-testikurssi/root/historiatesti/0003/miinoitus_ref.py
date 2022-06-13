import haravasto
import random

tila = {
    "kentta": None
}

def miinoita(kentta, parit, n):
    for c, r in random.sample(parit, n):
        kentta[r][c] = "x"
        
def piirra_kentta():
    haravasto.tyhjaa_ikkuna()
    haravasto.aloita_ruutujen_piirto()
    for r, rivi in enumerate(tila["kentta"]):
        for c, ruutu in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(ruutu, c * 40, r * 40)
    
    haravasto.piirra_ruudut()
    
def main():
    """Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän."""

    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(600, 400)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()

if __name__ == "__main__":
    kentta = []
    for rivi in range(10):
        kentta.append([])
        for sarake in range(15):
            kentta[-1].append(" ")
            
    jaljella = []
    for x in range(15):
        for y in range(10):
            jaljella.append((x, y))

    
    tila["kentta"] = kentta
    
    miinoita(kentta, jaljella, 35)
    main()
    




