""" Tulvataytto 
    Tällä ohjelmalla on tarkoitus etsiä ja vapauttaa toisiinsa
    kytkeytyneet turvalliset ruudut planeetalta
"""

import haravasto


def tulvataytto(kentta, x, y):
    """
    Merkitsee kentalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    lista = [(x, y)]

    while lista:
        
        (x, y) = lista[0]
        lista.pop(0)
        miinoja = 0
        alikentta = []

        
        
        if kentta[y][x] == " ":

            kentta[y][x] = "0"
                        
            """käydään läpi koordinatit (x,y) ympäriltä ja tarkastetaan onko
            koordinaatti jossakin reunassa"""
            #lasketaan tilan reunat (oletus että tila on matriisi)
            y_reuna = int(len(kentta) - 1)
            x_reuna = int(len(kentta[0]) - 1)
  
    
            # tarkistetaan koordinaattien sijainti
            if x == 0 and y == 0: #vasen yla_kulma
                dx1 = 0
                dx2 = 1
                dy1 = 0
                dy2 = 1

            elif 0 < x < x_reuna and y == 0: #yläreuna
                dx1 = 1
                dx2 = 1
                dy1 = 0
                dy2 = 1

            elif x == x_reuna and y == 0: #oikea yläkulma
                dx1 = 1
                dx2 = 0
                dy1 = 0
                dy2 = 1
            
            elif x == x_reuna and 0 < y < y_reuna: #oikea reuna
                dx1 = 1
                dx2 = 0
                dy1 = 1
                dy2 = 1
        
            elif x == x_reuna and y == y_reuna: #oikea alakulma
                dx1 = 1
                dx2 = 0
                dy1 = 1
                dy2 = 0
        
            elif 0 < x < x_reuna and y == y_reuna: #alareuna
                dx1 = 1
                dx2 = 1
                dy1 = 1
                dy2 = 0
        
            elif x == 0 and y == y_reuna: #vasen alakulma
                dx1 = 0
                dx2 = 1
                dy1 = 1
                dy2 = 0
        
            elif x == 0 and 0 < y < y_reuna: #vasen reuna
                dx1 = 0
                dx2 = 1
                dy1 = 1
                dy2 = 1
        
            elif 0 < x < x_reuna and 0 < y < y_reuna:#kaikki muut
                dx1 = 1
                dx2 = 1
                dy1 = 1
                dy2 = 1

            for i in range(y - dy1, y + dy2 + 1):
                rivi = kentta[i]
                for j in range(x - dx1, x + dx2 + 1):
                    if rivi[j] == "x":
                        miinoja = miinoja + 1
                    if kentta[i][j] == " ":
                        lista.append((j,i))

            kentta[y][x] = str(miinoja)
                
                        




