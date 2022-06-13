
laatikot = []


def luo_nappi(kehys, teksti, kasittelija):
    x = 0
    y = 0
    w = len(teksti) * 10
    h = 20
    laatikot.append((x, y, w, h, kasittelija))
    
def kaynnista():
    while True:
        for tapahtuma in hae_tapahtumat():
            if tapahtuma.tyyppi = "hiiri":
                for laatikko in laatikot:
                    if laatikko[0] <= hiiri.x < laatikko[0] + laatikko[2]:
                        if laatikko[1] <= hiiri.y < laatikko[1] + laatikko[3]:
                            laatikko[4]()
                           