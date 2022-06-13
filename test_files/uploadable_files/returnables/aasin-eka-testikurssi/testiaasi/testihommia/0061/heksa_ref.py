def muotoile_heksaluvuksi(luku, bitit):
    return hex(luku).replace("0x", "").rjust(bitit // 4, "0")

luku = int(input("Anna kokonaisluku: "))
tavut = int(input("Anna heksaluvun pituus: "))
print(muotoile_heksaluvuksi(luku, tavut))



    