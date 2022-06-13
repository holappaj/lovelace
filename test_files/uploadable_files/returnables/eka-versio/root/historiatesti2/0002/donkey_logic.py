"""
Määrittelee aasigotchin varsinaisen taustalla toimivan logiikan.
"""
import donkey_definitions as am

def init():
    """
    Alustaa aasidatan, eli luo uuden aasin sekä asettaa sen alkutilanteeseen.
    """
    aasidata = {
        "SATIATION": am.BEGIN,
        "HAPPINESS": am.BEGIN,
        "ENERGY": am.BEGIN,
        "AGE": 0,
        "MONEY": 0,
        "RETIREMENT": False,
    }
    return aasidata

def _age(aasidata):
    """
    Vanhentaa aasia ja jättää sen tarvittaessa eläkkeelle. Tarkoitettu vain
    moduulin sisäiseen käyttöön.
    """
    aasidata["AGE"] += 1
    
    if aasidata["AGE"] == am.RETIREMENTAGE:
        aasidata["RETIREMENT"] = True

def _update_states(aasidata):
    """
    Muuttaa aasin tiloja ajan kuluessa ja jättää aasin tarvittaessa
    sairaseläkkeelle. Tarkoitettu vain moduulin sisäiseen käyttöön.
    """
    if aasidata["AGE"] % 2 == 0:
        if aasidata["SATIATION"] > 6 and aasidata["ENERGY"] < am.MAX_STATE:
            aasidata["ENERGY"] += 1
        aasidata["SATIATION"] -= 1
    if aasidata["AGE"] % 3 == 0:
        aasidata["HAPPINESS"] -= 1
    
    if aasidata["SATIATION"] <= 0 or aasidata["HAPPINESS"] <= 0 or aasidata["ENERGY"] <= 0:
        aasidata["RETIREMENT"] = True

def feed(aasidata):
    """
    Ruokkii aasia, eli kasvattaa aasin kylläisyyttä, ellei se ole jo maksimissa.
    """
    _age(aasidata)
    _update_states(aasidata)
    if aasidata["SATIATION"] < am.MAX_STATE:
        aasidata["SATIATION"] += 1
    
def tickle(aasidata):
    """
    Kutittaa aasia, eli kasvattaa aasin onnellisuutta, ellei se ole jo maksimissa.
    """
    _age(aasidata)
    _update_states(aasidata)
    if aasidata["HAPPINESS"] < am.MAX_STATE:
        aasidata["HAPPINESS"] += 1

def work(aasidata):
    """
    Teettää aasilla töitä, eli vähentää aasin jaksamista rahapalkkaa vastaan.
    """
    _age(aasidata)
    aasidata["ENERGY"] -= 1
    aasidata["MONEY"] += 1
    _update_states(aasidata)