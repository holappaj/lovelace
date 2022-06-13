m = "yzafpnum kMGTPEZY"

def muuta_kerrannaisyksikko(v):
    n = v.rstrip(m)        
    p = v.lstrip("0123456789.e-")
    try:
        return float(n) * 10 ** (bool(p) * 3 * (m.find(p) - m.find(" ")))
    except ValueError:
        return None

while True:
    arvo = input("Anna muutettava arvo: ").strip()
    lukuarvo = muuta_kerrannaisyksikko(arvo)
    if lukuarvo != None:
        print(lukuarvo)
        break
    else:
        print("Arvo ei ole kelvollinen")
