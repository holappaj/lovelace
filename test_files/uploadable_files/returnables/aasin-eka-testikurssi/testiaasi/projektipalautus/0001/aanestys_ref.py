aanestys = {
    "jaa": 0,
    "ei": 0,
    "eos": 0,
    "virhe": 0
}

def aanesta(kysely):
    print("Anna äänesi, vaihtoehdot ovat:")
    print("jaa, ei, eos")
    aani = input(": ").lower()
    try:
        kysely[aani] += 1
    except KeyError:
        kysely["virhe"] += 1

def nayta_tulokset(kysely):
    tasoitus = max(len(avain) for avain in kysely.keys())
    for avain, arvo in kysely.items():
        print(avain.capitalize().ljust(tasoitus) + ":", arvo * "#")
    
aanesta(aanestys)
aanesta(aanestys)
aanesta(aanestys)
nayta_tulokset(aanestys)    
