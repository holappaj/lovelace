aanestys = {
    "yay": 0,
    "nay": 0,
    "idk": 0,
    "error": 0
}

def vote(kysely):
    print("Anna äänesi, vaihtoehdot ovat:")
    print("jaa, ei, eos")
    aani = input(": ").lower()
    try:
        kysely[aani] += 1
    except KeyError:
        kysely["error"] += 1

def show_results(kysely):
    tasoitus = max(len(avain) for avain in kysely.keys())
    for avain, arvo in kysely.items():
        print(avain.capitalize().ljust(tasoitus) + ":", arvo * "#")
    
vote(aanestys)
vote(aanestys)
vote(aanestys)
show_results(aanestys)    
