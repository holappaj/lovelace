def tarkista_alkuluku(luku):
    for i in range(2, int(luku ** 0.5) + 1):
        if luku % i == 0:
            return False
    return True

def pyyda_syote(kehoite, virheilmoitus):
    while True:
        try:
            syote = int(input(kehoite))
            if syote > 1:
                return syote
        except ValueError:
            pass
        print(virheilmoitus)

luku = pyyda_syote("Anna kokonaisluku, joka on suurempi kuin 1: ", "Pieleen meni :'(.")
if tarkista_alkuluku(luku):
    print("Kyseessä on alkuluku.")
else:
    print("Kyseessä ei ole alkuluku.")
