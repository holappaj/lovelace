import random
import re
import string

class RandomInt(object):
    
    def get_default(self):
        return str(0)    
    
    def __repr__(self):
        return str(random.randint(1, 1000))
    
    
class RandomFloat(object):
    
    def get_default(self):
        return str(0.0)
    
    def __repr__(self):
        return str(round(random.random() * 100, 2))


class RandomTimeStamp(object):

    def get_default(self):
        return repr("00:00:00")

    def __repr__(self):
        return repr("{:02}:{:02}:{:02}".format(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)))


INT_VALUE = 0
FLOAT_VALUE = 1
NAME_VALUE = 2
PLACE_VALUE = 3

RANDOM_SYMBOLS = ":.,;[()]-_"
ASCII_LOWER = "abcdefghijkmnopqstuvwxyz" # small letter l removed to avoid confusion with number 1 in some fonts
ASCII_ALL = ASCII_LOWER + string.ascii_uppercase

INT_VAR_NAMES = {
    "fi": ["lkm", "x", "y", "rivi", "sarake", "leveys", "korkeus", "indeksi", "n", "pisteet"],
    "en": ["count", "x", "y", "row", "column", "width", "height", "index", "n", "score"]
}

FLOAT_VAR_NAMES = {
    "fi": ["pituus", "nopeus", "paino", "kerroin", "energia", "kulma"],
    "en": ["length", "speed", "weight", "factor", "energy", "angle"]
}

NAME_VAR_NAMES = {
    "fi": ["nimi", "omistaja", "etunimi", "sukunimi", "alias", "voittaja", "pelaaja", "vastustaja"],
    "en": ["name", "owner", "given_name", "family_name", "alias", "winner", "player", "opponent"]
}

PLACE_VAR_NAMES = {
    "fi": ["sijainti", "kohde", "tapahtumapaikka"],
    "en": ["location", "destination", "venue"]
}

TIME_VAR_NAMES = {
    "fi": ["aika", "aikaleima", "vuoro", "framet", "sekunnit", "mikrosekunnit"],
    "en": ["time", "timestamp", "turn", "frames", "seconds", "microseconds"]
}

LOCATION_NAME_PAIRS = {
    "fi": [("x", "y"), ("rivi", "sarake"), ("x_sijainti", "y_sijainti"), ("leveysaste", "korkeusaste")],
    "en": [("x", "y"), ("row", "col"), ("x_pos", "y_pos"), ("latitude", "longitude")]
}

INPUT_VAR_NAMES = {
    "fi": ["rivi", "syote", "valinta", "tulos", "viesti", "komento"],
    "en": ["line", "reply", "choice", "result", "message", "command"]
}

SUM_VAR_NAMES = {
    "fi": ["summa", "tulos", "x_sijainti", "y_sijainti"],
    "en": ["total", "result", "x_pos", "y_pos"]
}

DIF_VAR_NAMES = {
    "fi": ["erotus", "x_sijainti", "y_sijainti"],
    "en": ["difference", "x_pos", "y_pos"]
}

MUL_VAR_NAMES = {
    "fi": ["nopeus", "sijainti", "tulo", "aika", "energia"],
    "en": ["speed", "location", "product", "time", "energy"]
}

DIV_VAR_NAMES = {
    "fi": ["tunnit", "minuutit", "nopeus", "rivi"],
    "en": ["hours", "minutes", "speed", "row"]
}

MOD_VAR_NAMES = {
    "fi": ["sarake", "indeksi", "jaannos", "ylijaama"],
    "en": ["column", "index", "remainder", "excess"]
}

INDEX_VAR_NAMES = {
    "fi": ["i", "j", "k"],
    "en": ["i", "j", "k"]
}

INT_LIST_NAMES = {
    "fi": ["pisteet", "tunnisteet", "koot", "valinnat", "arvosanat", "lottonumerot"],
    "en": ["points", "ids", "sizes", "choices", "grades", "lottery_numbers"]
}

FLOAT_LIST_NAMES = {
    "fi": ["vastusarvot", "mittaukset", "nopeudet", "kestot", "kulmat", "vektori", "suuntavektori"],
    "en": ["resistors", "measurements", "speeds", "durations", "angles", "vector", "unit_vector"]
}

NAME_LIST_NAMES = {
    "fi": ["nimet", "opiskelijat", "pelaajat", "osallistujat"],
    "en": ["names", "students", "players", "participants"]
}

RANGE_NAMES = {
    "fi": ["leveys", "korkeus", "lkm", "n"],
    "en": ["width", "height", "count", "n"]
}

RANDOM_NAMES = {
    "fi":  ["Muumipappa", "Hemuli", "Haisuli", "Nipsu", "Pikachu", "Bulbasaur", "Nalle Puh", "Ihaa", "Eunji", "Tomomi", "Haruna", "Seungyeon", "Ihsahn", "Abbath", "Fenriz", "Hessu", "Dolan", "Kappa", "doge", "Batman", "Odin"],
    "en": ["Hagrid", "Snape", "Dumbledore", "Luna", "Pikachu", "Bulbasaur", "Winnie", "Eeyore", "Eunji", "Tomomi", "Haruna", "Seungyeon", "Ihsahn", "Abbath", "Fenriz", "Goofy", "Dolan", "Kappa", "doge", "Batman", "Odin"]
}

RANDOM_PLACES = {
    "fi": ["muumitalo", "yliopisto", "aasinsilta", "Oulu", "ankat", "sorsapuisto"],
    "en": ["Hogwarts", "university", "Oulu", "roshpit", "jungle", "wormhole"]
}

SEQUENCE_NAMES = {
    "fi": ["syote", "sisalto", "vastukset", "inventaario", "ostokset", "osallistujat"],
    "en": ["sequence", "content", "resistors", "inventory", "shoplist", "participants"]
}

COMP_PAIR_NAMES = {
    "fi": [("x", "leveys"), ("y", "korkeus"), ("x_sijainti", "leveys"), ("y_sijainti", "korkeus"), ("rahat", "hinta"), ("pisteet", "ennatys"), ("rivi", "korkeus"), ("sarake", "leveys")],
    "en": [("x", "width"), ("y", "height"), ("x_pos", "width"), ("y_pos", "height"), ("money", "price"), ("score", "record"), ("row", "height"), ("col", "width")]
}

SEQUENCE_PAIR_NAMES = {
    "fi": [("elukat", "elukka"), ("kentta", "rivi"), ("komponentit", "komponentti"), ("kokoelma", "levy"), ("osallistujat", "nimi"), ("opiskelijat", "opiskelija"), ("inventaario", "esine")],
    "en": [("animals", "animal"), ("field", "row"), ("components", "component"), ("collection", "album"), ("participants", "name"), ("students", "student"), ("inventory", "item")]
}

SEQUENCE_MULTI_NAMES = {
    "fi": [
        ("pelaajat", ["nimi", "kasikortit", "pisteet"]), 
        ("koordinaatit", ["x", "y"]),
        ("arvostelu", ["opiskelija", "arvosana"]),
        ("inventaario", ["tavara", "n", "hinta"]),
        ("kokoelma", ["artisti", "nimi", "n", "kesto"]),
    ],
    "en": [
        ("players", ["name", "hand", "score"]),
        ("coordinates", ["x", "y"]),
        ("evaluation", ["student", "grade"]),
        ("inventory", ["item", "n", "price"]),
        ("collection", ["artist", "title", "n", "length"])
    ]
}

LIST_COPY_NAMES = {
    "fi": [
        ("alkuperaiset", "nykyiset"),
        ("kokoelma", "kopio"),
        ("kaikki_ruudut", "tyhjat"),
    ],
    "en": [
        ("original", "current"),
        ("collection", "copy"),
        ("all_tiles", "empty_tiles")
    ]
}
    
LIST_SLICE_NAMES = {
    "fi": [
        ("tulokset", "keski"),
        ("mittaukset", "leikkaus"),
        ("kaikki", "otanta"),
    ],
    "en": [
        ("results", "middle"),
        ("measurements", "slice"),
        ("all", "chosen")
    ]
}
    
DICT_NAMES_KEYS_VALUES = {
    "fi": 
        [
            ("mittaus", [("tulos", RandomFloat()), ("aika", RandomTimeStamp()), ("mittauslaite_id", RandomInt())]),
            ("hahmo", [("x", RandomInt()), ("y", RandomInt()), ("sprite_id", RandomInt()), ("anim_frame", RandomInt())]),
            ("ruutu", [("rivi", RandomInt()), ("sarake", RandomInt()), ("arvo", RandomInt())]),
            ("laatikko", [("x", RandomInt()), ("y", RandomInt()), ("leveys", RandomInt()), ("korkeus", RandomInt())]),
            ("koordinaatit", [("leveysaste", RandomFloat()), ("korkeusaste", RandomFloat()), ("korkeus_merenpinnasta", RandomFloat())]),            
        ]
    ,
    "en":
        [
            ("measurement", [("result", RandomFloat()), ("time", RandomTimeStamp()), ("device_id", RandomInt())]),
            ("character", [("x", RandomInt()), ("y", RandomInt()), ("sprite_id", RandomInt()), ("anim_frame", RandomInt())]),
            ("tile", [("row", RandomInt()), ("col", RandomInt()), ("value", RandomInt())]),
            ("rectangle", [("x", RandomInt()), ("y", RandomInt()), ("width", RandomInt()), ("height", RandomInt())]),
            ("coordinates", [("latitude", RandomFloat()), ("longitude", RandomFloat()), ("altitude", RandomFloat())]),
        ]
}
             
DICT_ITER_NAMES = {
    "fi":
        [("avain", "arvo"), ("kentta", "arvo"), ("k", "v"), ("ominaisuus", "arvo")],
    "en":
        [("key", "value"), ("field", "value"), ("k", "v"), ("property", "value")]
}
        
FUNC_NAMES_PARAMLESS = {
    "fi":
        ["main", "kysy_syote", "pyyda_komento", "luo_pakka", "tulosta_ohje"],
    "en":
        ["main", "prompt_input", "prompt_command", "create_deck", "print_instructions"]
}
        
FUNC_NAMES_PARAMS = {
    "fi": [
        (
            ["kysy_syote", "pyyda_syote", "kysy_arvo"], 
            [
                (("kysymys", "pyynto", "ohje", "kysymysteksti"), ": "),
                (("virhe", "virheviesti", "viesti", "huomautus"), "")
            ]
        ),
        (
            ["luo_kentta", "luo_pelialue", "luo_ikkuna", "muuta_ikkunaa", "aseta_suorakaide"],
            [
                (("leveys", "w", "pikselit_vaaka"), 640),
                (("korkeus", "h", "pikselit_pysty"), 480),
                (("x", "ylavasen_x", "vasen_reuna"), 0),
                (("y", "ylavasen_y", "ylareuna"), 0),
            ]
        ),
        (
            ["tulosta_valikko", "tulosta_valinnat", "tulosta_ohje"],
            [
                (("valinnat", "valikko", "vaihtoehdot", "ohje"), ""),
            ]
        ),
        (
            ["aseta_miina", "piirra_vastus", "luo_pelihahmo", "merkitse_piste"],
            [
                (("x", "sarake", "vaaka", "x_sijainti"), 0),
                (("y", "rivi", "pysty", "y_sijainti"), 0),
                (("kuvake", "sprite", "kuva", "ulkoasu"), ""),
            ]
        )                
    ],
    "en": [
        (
            ["ask_input", "prompt_input", "prompt_value"],
            [
                (("question", "request", "instruction", "prompt"), ": "),
                (("error", "errormsg", "message", "warning"), "")
            ]
        ),
        (
            ["create_field", "create_map", "create_window", "resize_window", "set_rectangle"],
            [
                (("width", "w", "horizontal_pixels"), 640),
                (("height", "h", "vertical_pixels"), 480),
                (("x", "topleft_x", "left_border"), 0),
                (("y", "topleft_y", "top_border"), 0),
            ]
        ),
        (
            ["print_menu", "print_choices", "print_instructions"],
            [
                (("choices", "menu", "options", "instructions"), ""),
            ]
        ),
        (
            ["set_mine", "draw_resistor", "create_character", "mark_point"],
            [
                (("x", "col", "horizontal", "x_pos"), 0),
                (("y", "row", "vertical", "y_pos"), 0),
                (("icon", "sprite", "image", "skin"), ""),
            ]
        )
    ]
}

MODULE_NAMES = ["math", "datetime", "json", "sys", "os", "random", "collections", "time"]

MODULE_NAMES_AS = [("math", "m"), ("numpy", "np"), ("random", "rand"), ("datetime", "dt"), ("time", "t"),]

COMP_OPS = [
    (">", "<"), 
    (">=", "<="),
    ("==", "=="),
    ("!=", "!="), 
    ("<=",">="),
    ("<", ">")
]

connectors = [ "and", "or",]

RE_TRANS = str.maketrans(
    {
        ".": "\\.",
        "^": "\\^",
        "$": "\\$",
        "*": "\\*",
        "+": "\\+",
        "?": "\\?",
        "{": "\\{",
        "}": "\\}",
        "[": "\\[",
        "]": "\\]",
        "|": "\\|",
        "(": "\\(",
        ")": "\\)",
        "'": "[\"']"
    }
)    

class AbsFunction(object):
    
    name = "abs"
    _names = {
        "fi": ["itseisarvo", "ero", "x_sijainti", "y_sijainti"],
        "en": ["absolute_value", "difference", "x_pos", "y_pos"]
    }

    @staticmethod
    def get_rv_name(lang):
        return random.choice(AbsFunction._names[lang])

    @staticmethod
    def gen_args(lang):
        return [round(random.random() * 100 - 50, 3)]


class IntFunction(object):
    
    name = "int"
    
    @staticmethod
    def get_rv_name(lang):
        return random.choice(INT_VAR_NAMES[lang])
    
    @staticmethod
    def gen_args(lang):
        return [round(random.random() * 100, 3)]

    
class LenFunction(object):

    name = "len"
    _names = {
        "fi": ["pituus", "lkm", "n"],
        "en": ["length", "count", "n"]
    }
    
    @staticmethod
    def get_rv_name(lang):
        return random.choice(LenFunction._names)
    
    @staticmethod
    def gen_args(lang):
        return random.choice(SEQUENCE_NAMES)
    
    
class RoundFunction(object):
    
    name = "round"
    
    @staticmethod
    def get_rv_name(lang):
        return random.choice(FLOAT_VAR_NAMES[lang])
    
    @staticmethod
    def gen_args(lang):
        args = [round(random.random() * 100, 8)]
        if random.randint(0, 1):
            args.append(random.randint(0, 6))
        return args
    
    
class MaxFunction(object):
    
    name = "max"
    _names = {
        "fi": ["maksimi", "suurin", "pisin"],
        "en": ["maximum", "largest", "longest"]
    }
    
    @staticmethod
    def get_rv_name(lang):
        return random.choice(MaxFunction._names[lang])
    
    @staticmethod
    def gen_args(lang):
        n = random.randint(2, 6)
        return [round(random.random() * 100, 2) for i in range(n)]
            

class DivmodFunction(object):
    
    name = "divmod"
    _names = {
        "fi": [("rivi", "sarake"), ("osamaara", "jakojaannos")],
        "en": [("row", "col"), ("quotient", "remainder")]
    }
    
    @staticmethod
    def get_rv_names(lang):
        return list(random.choice(DivmodFunction._names[lang]))
    
    @staticmethod
    def gen_args(lang):
        return [random.randint(0, 100), random.randint(1, 100)]
    
    
class BaseStrMethod(object):
    
    name = ""
    _names = {}

    @staticmethod
    def get_str(lang):
        return "".join(random.choices(ASCII_ALL, k=random.randint(10, 15)))
    
    @classmethod
    def get_rv_name(cls, lang):
        return random.choice(cls._names[lang])
    
    @staticmethod
    def gen_args(lang):
        return []
    
    @staticmethod
    def gen_comp(lang):
        raise NotImplementedError
        

class StrCapitalizeMethod(BaseStrMethod):
    
    name = "capitalize"
    _names = {
        "fi": ["otsikko", "nimike", "luokitus"],
        "en": ["header", "label", "tag"]
    }
    

class StrCountMethod(BaseStrMethod):
    
    name = "count"
    _names = {
        "fi": ["lkm", "n", "maara"],
        "en": ["count", "n"]
    }

    @staticmethod
    def gen_args(lang):
        return [random.choice(ASCII_ALL)]

    @staticmethod
    def gen_comp(lang):
        return random.randint(0, 10)


class StrEndswithMethod(BaseStrMethod):
    
    name = "endswith"
    _names = {
        "fi": ["loppu", "paattyy", "tarkistus"],
        "en": ["end", "ends", "check"]
    }

    @staticmethod
    def gen_args(lang):
        return [random.choice(RANDOM_SYMBOLS)]
    
    @staticmethod
    def gen_comp(lang):
        return random.choice((True, False))


class StrLjustMethod(BaseStrMethod):
    
    name = "ljust"
    _names = {
        "fi": ["sarake", "tietue", "arvo", "aika", "hinta", "paino", "lkm", "sisalto"],
        "en": ["column", "col", "value", "time", "price", "weight", "count", "content"]
    }

    @staticmethod
    def get_str(lang):
        return "{:.{}f}".format(random.random() * 100, random.randint(2, 4))

    @staticmethod
    def gen_args(lang):
        return random.randint(8, 20)


class StrLowerMethod(BaseStrMethod):

    name = "lower"
    _names = INPUT_VAR_NAMES

    @staticmethod
    def gen_comp(lang):
        return random.choice(ASCII_LOWER)

class StrReplaceMethod(BaseStrMethod):
    
    name = "replace"
    _names = INPUT_VAR_NAMES
    
    @classmethod
    def gen_args(cls, lang):
        #if random.randint(0, 3):
        if False:
            args = random.sample(ASCII_LOWER, 2)
            cls.comp = args[1] * random.randint(4, 8)
            return args
        else:
            args = random.sample(ASCII_LOWER, 2) + [random.randint(1, 3)]
            cls.comp = args[1] * args[2] + args[0] * random.randint(1, 3)
            return args

    @classmethod
    def gen_comp(cls, lang):
        return cls.comp

class StrRjustMethod(BaseStrMethod):
    
    name = "rjust"
    _names = {
        "fi": ["sarake", "tietue", "arvo", "aika", "hinta", "paino", "lkm", "sisalto"],
        "en": ["column", "col", "value", "time", "price", "weight", "count", "content"]
    }

    @staticmethod
    def get_str(lang):
        return "{:.{}f}".format(random.random() * 100, random.randint(2, 4))

    @staticmethod
    def gen_args(lang):
        return random.randint(8, 20)


class StrRstripMethod(BaseStrMethod):

    name = "rstrip"
    _names = INPUT_VAR_NAMES

    @staticmethod
    def gen_comp(lang):
        return "".join(random.choices(ASCII_ALL, k=random.randint(10, 15)))


class StrStartswithMethod(BaseStrMethod):

    name = "startswith"
    _names = {
        "fi": ["alkaa", "alku", "tarkistus"],
        "en": ["starts", "start", "check"]
    }

    @staticmethod
    def gen_args(lang):
        return [random.choice(RANDOM_SYMBOLS)]

    @staticmethod
    def gen_comp(lang):
        return random.choice((True, False))


class StrStripMethod(BaseStrMethod):

    name = "strip"
    _names = INPUT_VAR_NAMES

    @staticmethod
    def gen_comp(lang):
        return "".join(random.choices(ASCII_ALL, k=random.randint(10, 15)))


class StrTitleMethod(BaseStrMethod):

    name = "title"
    _names = {
        "fi": ["otsikko", "nimike", "luokitus"],
        "en": ["header", "label", "tag"]
    }


class StrUpperMethod(BaseStrMethod):

    name = "upper"
    _names = INPUT_VAR_NAMES

    @staticmethod
    def gen_comp(lang):
        return random.choice(ASCII_LOWER).upper()


class StrZfillMethod(BaseStrMethod):
    
    name = "zfill"
    _names = {
        "fi": ["pisteet", "tulos", "osoite", "muistipaikka"],
        "en": ["score", "result", "address", "memaddr"]
    }
    
    @staticmethod
    def gen_args(lang):
        return str(random.randint(1, 100))

class MathModule(object):
    
    name = "math"
    alias = "m"
    _callables = ["sin", "cos", "tan", "radians", "degrees", "asin", "acos", "atan", "ceil", "floor", "log10", "log1p"]
    
    def get_names(self):
        import math
        names = [n for n in dir(math) if not n.startswith("__")]
        return random.sample(names, random.randint(1, 3))
    
    def get_function_call(self, lang):
        fname = random.choice(self._callables)
        args = [round(random.random() * 100, 2)]
        if lang == "fi":
            varname = "tulos"
        else:
            varname = "result"
        return fname, args, varname
    

class RandomModule(object):
    
    name = "random"
    alias = "rand"
    _callables = ["randint", "random"]
    
    def get_names(self):
        import random
        names = [n for n in dir(random) if n.islower() and not n.startswith("__")]
        return random.sample(names, random.randint(1, 3))
    
    def get_function_call(self, lang):
        fname = random.choice(self._callables)
        if lang == "fi":
            varname = "tulos"
        else:
            varname = "result"
        
        if fname == "randint":
            a = random.randint(0, 10)
            b = random.randint(a + 1, 100)
            args = [a, b]            
        elif fname == "random":
            args = []

        return fname, args, varname


class TimeModule(object):
    
    name = "time"
    alias = "t"
    _callables = ["time", "sleep", "localtime"]
    
    def get_names(self):
        import time
        names = [n for n in dir(time) if n.islower() and not n.startswith("__")]
        return random.sample(names, random.randint(1, 3))
    
    def get_function_call(self, lang):
        raise NotImplementedError


class DatetimeModule(object):
    
    name = "datetime"
    alias = "dt"
    _callables = []
    
    def get_names(self):
        import datetime
        names = [n for n in dir(datetime) if not n.startswith("__")]
        return random.sample(names, random.randint(1, 3))
    
    def get_function_call():
        raise NotImplementedError
    
    
class JsonModule(object):
    
    name = "json"
    alias = "js"

    def get_names(self):
        import json
        names = [n for n in dir(json) if n.islower() and not n.startswith("__")]
        return random.sample(names, random.randint(1, 3))
        
    def get_function_call():
        raise NotImplementedError


class SysModule(object):
    
    name = "sys"
    alias = "sys"
    _callables = []
    
    def get_names(self):
        import sys
        names = [n for n in dir(sys) if n.islower() and not n.startswith("__")]
        return random.sample(names, random.randint(1, 3))
        
    def get_function_call():
        raise NotImplementedError
    
    
class OsModule(object):
    
    name = "os"
    alias = "os"
    _callables = []
    
    def get_names(self):
        import os
        names = [n for n in dir(os) if n.islower() and not n.startswith("__")]
        return random.sample(names, random.randint(1, 3))
        
    def get_function_call():
        raise NotImplementedError
    
    
    


SINGLE_RETURN_FUNCTIONS = [AbsFunction, IntFunction, RoundFunction, MaxFunction]
CONDITION_FUNCTIONS = [AbsFunction, RoundFunction, MaxFunction, LenFunction]
CONDITION_METHODS_RV_ARG = [StrCountMethod, StrReplaceMethod]
CONDITION_METHODS_RV_NOARG = [] #[StrLowerMethod, StrRstripMethod, StrStripMethod, StrUpperMethod]
CONDITION_METHODS_BOOL = [StrEndswithMethod, StrStartswithMethod]
METHODS_RV_ARG = [StrCountMethod, StrReplaceMethod, StrLjustMethod, StrRjustMethod, StrZfillMethod]
METHODS_RV_NOARG = [StrCapitalizeMethod, StrLowerMethod, StrRstripMethod, StrStripMethod, StrTitleMethod, StrUpperMethod]
MULTI_RETURN_FUNCTIONS = [DivmodFunction]
MODULES = [MathModule, RandomModule, TimeModule, DatetimeModule, OsModule, SysModule, JsonModule]
CALLABLE_MODULES = [MathModule, RandomModule]

FLOAT_SPEC = 1
INT_SPEC = 2

class SimpleFormatTemplate(object):
    
    _spec_re = re.compile(r"__[a-z0-9_]+__[a-z]__")
    
    _templates = {
        "fi": [
            ("Tulos: __tulos__f__", FLOAT_VAR_NAMES["fi"]),
            ("Sijainti: __s0__d__, __s1___d__", LOCATION_NAME_PAIRS["fi"]),
            ("Arvo hetkella __aika__d__: __arvo__f__", TIME_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
            ("Hetkella __aika__d__ sijainti on __s0__d__, __s1__d__", TIME_VAR_NAMES["fi"], LOCATION_NAME_PAIRS["fi"]),
            ("Henkilon __nimi__s__ tulos: __tulos__f__", NAME_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
            ("Mittaustulos __tulos__f__ sijainnissa __paikka__s__", FLOAT_VAR_NAMES["fi"], PLACE_VAR_NAMES["fi"]),
            ("Listan __indeksi__d__. henkilo on __nimi__s__", INDEX_VAR_NAMES["fi"], NAME_VAR_NAMES["fi"]),
            ("Ruudussa (__s0__d__, __s1__d__) on __nimi__s__", LOCATION_NAME_PAIRS["fi"], NAME_VAR_NAMES["fi"]),
            ("Kierros __indeksi__d__ / __n__d__", INDEX_VAR_NAMES["fi"], RANGE_NAMES["fi"]),
            ("Mitattu: __mittaus__f__ (__tila__f__)", FLOAT_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
            ("Valitulos: __tulos__f__ (__indeksi__d__ / __n__d__)", FLOAT_VAR_NAMES["fi"], INDEX_VAR_NAMES["fi"], RANGE_NAMES["fi"]),
            ("Arvo kohdassa __piste_x__f__: __piste_y__f__", FLOAT_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
            ("Tulosten valinen ero: __erotus__f__", DIF_VAR_NAMES["fi"]),
            ("Saatu tulo: __tulo__f__", MUL_VAR_NAMES["fi"]),
            ("Hemulin ominaisuudet: __o1__f__, __o2__f__, __o3__d__", FLOAT_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"], INT_VAR_NAMES["fi"]),
            ("Mita saadaan kun __luku_1__f__ kerrotaan luvulla __luku_2__d__", FLOAT_VAR_NAMES["fi"], INT_VAR_NAMES["fi"]),
            ("Laske yhteen luvut __luku_1__f__ ja __luku_2__d__", FLOAT_VAR_NAMES["fi"], INT_VAR_NAMES["fi"]),
            ("Vahenna __luku_1__d__ luvusta __luku_2__f__", INT_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
        ],

        "en": [
            ("Result: __Result__f__", FLOAT_VAR_NAMES["fi"]),
            ("Location: __s0__d__, __s1___d__", LOCATION_NAME_PAIRS["fi"]),
            ("Value at the moment of __time__d__: __value__f__", TIME_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
            ("At the moment __aika__d__ location is __s0__d__, __s1__d__", TIME_VAR_NAMES["fi"], LOCATION_NAME_PAIRS["fi"]),
            ("Person __name__s__ result: __result__f__", NAME_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
            ("Measurement result __result__f__ at location __location__s__", FLOAT_VAR_NAMES["fi"], PLACE_VAR_NAMES["fi"]),
            ("Lists __index__d__. person is __name__s__", INDEX_VAR_NAMES["fi"], NAME_VAR_NAMES["fi"]),
            ("In the square (__s0__d__, __s1__d__) is __name__s__", LOCATION_NAME_PAIRS["fi"], NAME_VAR_NAMES["fi"]),
            ("Lap __index__d__ / __n__d__", INDEX_VAR_NAMES["fi"], RANGE_NAMES["fi"]),
            ("Measured: __measurement__f__ (__status__f__)", FLOAT_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
            ("Interdemiate result: __result__f__ (__index__d__ / __n__d__)", FLOAT_VAR_NAMES["fi"], INDEX_VAR_NAMES["fi"], RANGE_NAMES["fi"]),
            ("Value at location __point_x__f__: __point_y__f__", FLOAT_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
            ("Difference between the results: __difference__f__", DIF_VAR_NAMES["fi"]),
            ("Result gained: __result__f__", MUL_VAR_NAMES["fi"]),
            ("Hagrids qualities: __o1__f__, __o2__f__, __o3__d__", FLOAT_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"], INT_VAR_NAMES["fi"]),
            ("What do we get when __num_1__f__ is multiplied by __num_2__d__", FLOAT_VAR_NAMES["fi"], INT_VAR_NAMES["fi"]),
            ("Add together numbers __num_1__f__ and __num_2__d__", FLOAT_VAR_NAMES["fi"], INT_VAR_NAMES["fi"]),
            ("Substract __num_1__d__ from __num_2__f__", INT_VAR_NAMES["fi"], FLOAT_VAR_NAMES["fi"]),
        ]
    }
    
    def __init__(self, lang, kws=False):
         tmpl_spec = random.choice(self._templates[lang])
         self.template = tmpl_spec[0]
         self.name_groups = tmpl_spec[1:]
         self.minlength = random.randint(2, 6)
         self.decimals = random.randint(1, 4)
         self.names = []
         for group in self.name_groups:
             choice = random.choice(group)
             if isinstance(choice, str):
                 self.names.append(choice)
             else:
                 self.names.extend(choice)
   
    def get_var_names(self, kws=False):
        if not kws:
            return self.names
        else:
            keywords = []
            placeholders = self._spec_re.findall(self.template)
            for pattern in placeholders:
                keyword = pattern.split("__")[1]
                if keyword not in keywords:
                    keywords.append(keyword)
                    
            return zip(keywords, self.names)
    
    def get_string(self, kws=False):
        if not kws:
            return repr(self._spec_re.sub("___", self.template))
        else:
            r_str = self.template
            placeholders = self._spec_re.findall(self.template)
            for pattern in placeholders:
                r_str = r_str.replace(pattern, "_" + pattern.split("__")[1] + "_")
            
            return repr(r_str)
    
    def get_float_spec(self):
        placeholders = self._spec_re.findall(self.template)
        float_names = []
        for i, pattern in enumerate(placeholders):            
            name, vtype = pattern.split("__")[1:3]
            if vtype == "f":
                float_names.append(self.names[i])
            
        return float_names, self.decimals
        
    def get_int_spec(self):
        placeholders = self._spec_re.findall(self.template)
        int_names = []
        for i, pattern in enumerate(placeholders):            
            name, vtype = pattern.split("__")[1:3]
            if vtype == "d":
                int_names.append(self.names[i])
            
        return int_names, self.minlength
        
    
    def get_rex(self, kws=False, spec=None):
        if not kws and not spec:
            rex = self._spec_re.sub("{}", self.template)
        elif kws and not spec:
            rex = self.template
            placeholders = self._spec_re.findall(self.template)
            for pattern in placeholders:            
                rex = rex.replace(pattern, "{" + pattern.split("__")[1] + "}")
        
        elif not kws and spec == FLOAT_SPEC:
            rex = self.template
            placeholders = self._spec_re.findall(self.template)
            for pattern in placeholders:        
                name, vtype = pattern.split("__")[1:3]
                if vtype == "f":
                    rex = rex.replace(pattern, "{:." + str(self.decimals) + "f}")
                else:
                    rex = rex.replace(pattern, "{}")
        
        elif not kws and spec == INT_SPEC:
            rex = self.template
            placeholders = self._spec_re.findall(self.template)
            for pattern in placeholders:        
                name, vtype = pattern.split("__")[1:3]
                if vtype == "d":
                    rex = rex.replace(pattern, "{:>£0" + str(self.minlength) + "d£}")
                else:
                    rex = rex.replace(pattern, "{}")
        
        elif kws and spec == FLOAT_SPEC:
            rex = self.template
            placeholders = self._spec_re.findall(self.template)
            for pattern in placeholders:        
                name, vtype = pattern.split("__")[1:3]
                if vtype == "f":
                    rex = rex.replace(pattern, "{" + name + ":." + str(self.decimals) + "f}")
                else:
                    rex = rex.replace(pattern, "{" + name + "}")
            
        elif kws and spec == INT_SPEC:
            rex = self.template
            placeholders = self._spec_re.findall(self.template)
            for pattern in placeholders:        
                name, vtype = pattern.split("__")[1:3]
                if vtype == "d":
                    rex = rex.replace(pattern, "{" + name + ":>£0" + str(self.minlength) + "d£}")
                else:
                    rex = rex.replace(pattern, "{" + name + "}")
        
        
        return rex.translate(RE_TRANS).replace(" ", " *").replace("£", "?")
        
            
        
        




