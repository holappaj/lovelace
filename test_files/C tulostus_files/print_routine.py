import json
import random
import test_core as core
import re

PRINTF_CSV = 0
SPRINTF_CSV = 1
PRINTF = 2
SPRINTF = 3

nums_short = [
    {"fi": "yksi", "fi:lla": "yhdellä", "fi:een": "yhteen", "en": "one", "num": 1},
    {"fi": "kaksi", "fi:lla": "kahdella", "fi:een": "kahteen", "en": "two", "num": 2},
    {"fi": "kolme", "fi:lla": "kolmella", "fi:een": "kolmeen", "en": "three", "num": 3},
    {"fi": "neljä", "fi:lla": "neljällä", "fi:een": "neljään", "en": "four", "num": 4}
]

nums_long = [
    {"fi": "viisi", "fi:lla": "viidellä", "en": "five", "num": 5},
    {"fi": "kuusi", "fi:lla": "kuudella", "en": "six", "num": 6},
    {"fi": "seitsemän", "fi:lla": "seitsemällä", "en": "seven", "num": 7},
    {"fi": "kahdeksan", "fi:lla": "kahdeksalla", "en": "eight", "num": 8},
    {"fi": "yhdeksän", "fi:lla": "yhdeksällä", "en": "nine", "num": 9}
]

class TypeClass:
    def __init__(self, forms_fi, forms_en, formStr, formUnsign, cType=[], unsignCType=[]):
        self.forms_fi = forms_fi
        self.forms_en = forms_en
        self.formStr = formStr
        self.formUnsign = formUnsign
        self.cType = cType
        self.unsignCType = unsignCType

    def randPos(self, lang):
        pos = {
            "fi": ["etumerkitön "],
            "en": ["unsigned "]
        }
        # 50% chance
        isPos = random.randint(0, 1) == 0
        return [random.choice(pos[lang]) if isPos else "", isPos]

    def get(self, lang):
        # choose spec string based on language
        if lang == "fi":
            s = random.choice(self.forms_fi)
        else:
            s = random.choice(self.forms_en)

        pos = self.randPos(lang)
        short_num = random.choice(nums_short)
        s = s.format(n=short_num[lang], nlla=short_num["fi:lla"], pos=pos[0])
        f = [self.formStr, self.formUnsign][pos[1]].format(n=short_num["num"]) # format string part
        return s, f, random.choice([self.cType, self.unsignCType][pos[1]])

    def get2(self, typeclass, lang):
        # choose spec string based on language
        if lang == "fi":
            s = random.choice(self.forms_fi)
        else:
            s = random.choice(self.forms_en)

        typeDesc = typeclass.get(lang)
        pos = self.randPos(lang)
        long_num = random.choice(nums_long)
        s = s.format(n=long_num[lang], nlla=long_num["fi:lla"], pos=pos[0], tyyppi=typeDesc[0])
        f = [self.formStr, self.formUnsign][pos[1]].format(n=long_num["num"],
                d_type=typeDesc[1].replace('%', '')) # format string part
        return s, f, typeDesc[2]


# standard print types
types = [
    TypeClass(["{n}desimaalinen yksinkertaisen tarkkuuden liukuluku", "yksinkertaisen tarkkuuden liukuluku {nlla} desimaalilla"],
        ["a single precision floating point number with {n} decimals", "a {n}-decimal single precision floating point number"],
        "%\.{n}f", "%\.{n}f", ["float"], ["float"]),
    TypeClass(["{n}desimaalinen kaksinkertaisen tarkkuuden liukuluku", "kaksinkertaisen tarkkuuden liukuluku {nlla} desimaalilla"],
        ["a double precision floating point number with {n} decimals", "a {n}-decimal double precision floating point number"],
        "%\.{n}l?f", "%\.{n}l?f", ["double"], ["double"]),
    TypeClass(["{pos}kokonaisluku"], ["a {pos}integer"], '(%(d|i)|%"\s*PRI(d|i)32\s*")', '(%u|%"\s*PRIu32\s*")', ["int"], ["unsigned int"]),
    TypeClass(["{pos}16-bittinen kokonaisluku"], ["a {pos}16 bit integer"], '(%h(d|i)|%"\s*PRI(d|i)16\s*")', '(%hu|%"\s*PRIu16\s*")', ["short", "short int", "int16_t"], ["unsigned short", "unsigned short int", "uint16_t"]),
    TypeClass(["{pos}64-bittinen kokonaisluku"], ["a {pos}64 bit integer"], '(%l(d|i)|%"\s*PRI(d|i)64\s*")', '(%lu|%"\s*PRIu64\s*")', ["int64_t"], ["uint64_t"]),
]

# prints with extra flags, containing a type
extras = [
    TypeClass(["{tyyppi} vähintään {n}merkkisessä kentässä välilyönneillä vasemmalta täytettynä"],
        ["{tyyppi} right-aligned using spaces within a field with a minimum width of {n}"], "%{n}{d_type}",
        "%{n}{d_type}"),
    TypeClass(["{tyyppi} vähintään {n}merkkisessä kentässä välilyönneillä oikealta täytettynä"],
        ["{tyyppi} left-aligned using spaces within a field with a minimum width of {n}"], "%-{n}{d_type}",
        "%-{n}{d_type}"),
    TypeClass(["{tyyppi} vähintään {n} merkkiä pitkässä kentässä etunollilla täytettynä", "{n} merkkiä pitkässä kentässä etunollilla täytettynä oleva {tyyppi}"],
        ["{tyyppi} zero padded to have a minimum field width of {n}"], "%0{n}{d_type}",
        "%0{n}{d_type}"),
    TypeClass(["{tyyppi} etumerkillä (+ tai -) varustettuna"], ["{tyyppi} with a sign (+ or -)"], "%\+{d_type}",
    "%\+{d_type}")
]

names = ["temp", "humid", "press", "light", "time"]

def getTypeSpec(lang):
    # 60 % chance for a single type, 40 % chance for additional flags
    rand = random.randint(1, 5)
    type1 = random.choice(types)
    if rand >= 4: # get additional flag types
        extra = random.choice(extras)
        form = extra.get2(type1, lang) # extra contains type type1
    else:
        form = type1.get(lang)
    return form # str, typedef

templates = {
    "fi": [
        [ # PRINTF_CSV
            """Kirjoita {{{{{{printf}}}}}}-kutsu, jolla tulostetaan pilkulla erotettuna (CSV) muuttujien {{{{{{x}}}}}}, {{{{{{y}}}}}} ja {{{{{{z}}}}}} arvot. Tässä {{{{{{x}}}}}} on {xFormat}, {{{{{{y}}}}}} on {yFormat} ja {{{{{{z}}}}}} on {zFormat}.

Tämä tulostus ei pääty rivinvaihtoon."""
        ],
        [ # SPRINTF_CSV: n-merkkiä pitkä CSV kaksidesimaalisilla arvoilla, jokaisessa yhtä leveä kenttä, arvot vähemmän kuin 100
            """Kirjoita muuttujaan {{{{{{str}}}}}} merkkijono, jossa on pilkulla erotettuna (CSV) liukulukumuuttujien {{{{{{x}}}}}}, {{{{{{y}}}}}} ja {{{{{{z}}}}}} arvot. Osoitteeseen {{{{{{str}}}}}} on allokoitu tilaa {n} tavulle, ja tämä täytyy täyttää kokonaan käyttämällä enintään yhtä montaa etunollaa kullekin arvolle. Tässä kaikki arvot pyöristetään {desimaaleja} desimaaliin ja muuttujat {{{{{{x,y,z}}}}}} ovat pienempiä kuin {zeros_max}. Muista ottaa huomioon merkkijonon päättävä nollatavu!

Tässä merkkijonossa ei ole rivinvaihtoa."""
        ],
        [ # PRINTF: Specsataan muuttujien tyypit ja tulostetaan ne key-value muodossa
            """Kirjoita {{{{{{printf}}}}}}-kutsu, jolla tulostetaan muuttujat
{{{{{{highlight=c
{typeX} x; // {nimiX}
{typeY} y; // {nimiY}
{typeZ} z; // {nimiZ}
}}}}}}
nimi:arvo-pareina pilkulla erotettuna. Muuttujan {{{{{{x}}}}}} nimi on '{nimiX}', muuttujan {{{{{{y}}}}}} '{nimiY}', ja muuttujan {{{{{{z}}}}}} '{nimiZ}'. Tulostetaan nämä siten, että {{{{{{x}}}}}} on {xFormat}, {{{{{{y}}}}}} on {yFormat} ja {{{{{{z}}}}}} on {zFormat}.

Tämän tulostuksen lopussa on rivinvaihto."""
        ],
        [ # SPRINTF:
            """Kirjoita muuttujaan {{{{{{str}}}}}} merkkijono, jossa on pilkulla erotettuna nimi:arvo-parit muuttujille
{{{{{{highlight=c
{typeX} x; // {nimiX}
{typeY} y; // {nimiY}
{typeZ} z; // {nimiZ}
}}}}}}
Muuttujan {{{{{{x}}}}}} nimi on '{nimiX}', muuttujan {{{{{{y}}}}}} '{nimiY}', ja muuttujan {{{{{{z}}}}}} '{nimiZ}'. Tulostetaan nämä siten, että {{{{{{x}}}}}} on {xFormat}, {{{{{{y}}}}}} on {yFormat} ja {{{{{{z}}}}}} on {zFormat}.

Tässä merkkijonossa ei ole rivinvaihtoa."""
        ]
    ],
    "en": [ # ENGLISH:
    
        [ # PRINTF_CSV
            """Write a {{{{{{printf}}}}}} call, which prints the values of variables {{{{{{x}}}}}}, {{{{{{y}}}}}}, and {{{{{{z}}}}}}, as comma separated values (CSV). Here {{{{{{x}}}}}} is {xFormat}, {{{{{{y}}}}}} is {yFormat}, and {{{{{{z}}}}}} is {zFormat}.

This print doesn't end with a newline."""
        ],
        [ # SPRINTF_CSV
            """Write a string into the variable {{{{{{str}}}}}}, where are the comma separated values of the floating point numbers {{{{{{x}}}}}}, {{{{{{y}}}}}}, and {{{{{{z}}}}}}. We have allocated {n} bytes of space in the address {{{{{{str}}}}}}, and this has to be completely filled by using at most equally many leading zeros for each value. Here all values are rounded to {decimals} decimals, and the variables {{{{{{x,y,z}}}}}} are smaller than {zeros_max}. Remember to take into account the zero byte ending the string!

This string doesn't include a newline."""
        ],
        [ # PRINTF
            """Write a {{{{{{printf}}}}}} call, which prints the variables
{{{{{{highlight=c
{typeX} x; // {nimiX}
{typeY} y; // {nimiY}
{typeZ} z; // {nimiZ}
}}}}}}
as name:value pairs separated by commas. The name of the variable {{{{{{x}}}}}} is '{nimiX}', the name of {{{{{{y}}}}}} is '{nimiY}', and the name of {{{{{{z}}}}}} is '{nimiZ}'. We will print these such that {{{{{{x}}}}}} is {xFormat}, {{{{{{y}}}}}} is {yFormat}, and {{{{{{z}}}}}} is {zFormat}.

The print ends with a newline."""
        ],
        [ # SPRINTF
            """Write into the variable {{{{{{str}}}}}} a string, which contains the comma separated name:value pairs for the variables
{{{{{{highlight=c
{typeX} x; // {nimiX}
{typeY} y; // {nimiY}
{typeZ} z; // {nimiZ}
}}}}}}
The name of variable {{{{{{x}}}}}} is '{nimiX}', the name of {{{{{{y}}}}}} is '{nimiY}', and of {{{{{{z}}}}}} '{nimiZ}'. We will print these such that {{{{{{x}}}}}} is {xFormat}, {{{{{{y}}}}}} is {yFormat}, and {{{{{{z}}}}}} is {zFormat}.

This string doesn't include a newline."""
        ]
    ]
}

def determine_question(history, completed, active):
    '''
    Determines what and if a question needs to be asked. 
    - Depends on cmd line argument and the amount of correct questions answered.
    '''
    required_repeats = 1

    if completed:
        return random.choice(active), None, None

    choices = []
    remaining = 0
    done = 0
    for cq in active:
        correct = history.count([cq, True])
        incorrect = history.count([cq, False])
        done += correct
        if correct < required_repeats or correct <= incorrect:
            choices.append(cq)
            remaining += max(required_repeats - correct, incorrect - correct)
            #remaining += max(required_repeats - correct, incorrect - correct)

    return random.choice(choices), done, min(done + remaining, 8)

def generate_params(question_class, lang):
    '''
    - Generates all the parameters that are used in the questions. 
    - Returns them as a dictionary.
    - When parameters come in a list it also creates a formated dictionary
      where list is changed into a string.
    '''
    template = random.choice(templates[lang][question_class])
    if question_class == PRINTF_CSV:        
        xFormat = getTypeSpec(lang)
        yFormat = getTypeSpec(lang)
        zFormat = getTypeSpec(lang)
        question = template.format(xFormat=xFormat[0], yFormat=yFormat[0], zFormat=zFormat[0])
        # Gets rid of the empty string at the end: (%(d|i)|%"\s*PRI(d|i)16\s*")" to (%(d|i)"|%"\s*PRI(d|i)16)
        if zFormat[1].endswith('")'):
            if zFormat[1][1:].find('%') > -1:
                zForm = zFormat[1].replace('|%', '"|%').replace('\s*")', '(\s*"")*)')
            else:
                zForm = zFormat[1].replace('|"\s', '"|"\s').replace('\s*")', '(\s*"")*)')
            # '(%(d|i)|%"\s*PRI(d|i)32\s*")', '(%u|%"\s*PRIu32\s*")'
            answer = "printf\s*\(\s*\"" + ",".join([xFormat[1], yFormat[1], zForm]) + "\s*,\s*x\s*,\s*y\s*,\s*z\s*\)\s*;"
        else:
            answer = "printf\s*\(\s*\"" + ",".join([xFormat[1], yFormat[1], zFormat[1]]) + "\"\s*,\s*x\s*,\s*y\s*,\s*z\s*\)\s*;"
        raw = {
            "question": question,
            "answer": answer
        }
        return raw, raw

    # 00.53,00.62,00.24z: neccessary bytes 6, decimals 3*n, zeros 3*k -> 18 chars
    elif question_class == SPRINTF_CSV:
        decimals = random.choice(nums_short)
        zeros_max = random.randint(2, 4)
        n = 6 + 3*(decimals["num"] + zeros_max)
        zeros_max = zeros_max
        question = template.format(n=n, desimaaleja=decimals["fi:een"], decimals=decimals["en"], zeros_max=10**zeros_max)
        zeros_max += decimals["num"]+1
        answer = "sprintf\s*\(\s*str\s*,\s*\"" + ",".join([f"%0{zeros_max}.{decimals['num']}f" for k in range(3)]) + "\"\s*,\s*x\s*,\s*y\s*,\s*z\s*\)\s*;"
        raw = {
            "question": question,
            "answer": answer
        }
        return raw, raw

    elif question_class == PRINTF:
        xFormat = getTypeSpec(lang)
        yFormat = getTypeSpec(lang)
        zFormat = getTypeSpec(lang)
        nimiX, nimiY, nimiZ = random.sample(names, 3)
        question = template.format(typeX=xFormat[2], typeY=yFormat[2], typeZ=zFormat[2],
                nimiX=nimiX, nimiY=nimiY, nimiZ=nimiZ, xFormat=xFormat[0], yFormat=yFormat[0],
                zFormat=zFormat[0])
        answer = "printf\s*\(\s*\"" + ",".join([nimiX + ":" + xFormat[1], nimiY + ":" + yFormat[1], nimiZ + ":" + zFormat[1]]) + "\\\n\"\s*,\s*x\s*,\s*y\s*,\s*z\s*\)\s*;"
        raw = {
            "question": question,
            "answer": answer
        }
        return raw, raw
    
    elif question_class == SPRINTF:
        xFormat = getTypeSpec(lang)
        yFormat = getTypeSpec(lang)
        zFormat = getTypeSpec(lang)
        nimiX, nimiY, nimiZ = random.sample(names, 3)
        question = template.format(typeX=xFormat[2], typeY=yFormat[2], typeZ=zFormat[2],
                nimiX=nimiX, nimiY=nimiY, nimiZ=nimiZ, xFormat=xFormat[0], yFormat=yFormat[0],
                zFormat=zFormat[0])
        #answer = "sprintf\(str,\s*\"" + ",".join([nimiX + ":" + xFormat[1], nimiY + ":" + yFormat[1], nimiZ + ":" + zFormat[1]]) + "\",\s*x,\s*y,\s*z\);"
        # Gets rid of the empty string at the end: (%(d|i)|%"\s*PRI(d|i)16\s*")" to (%(d|i)"|%"\s*PRI(d|i)16)
        if zFormat[1].endswith('")'):
            if zFormat[1][1:].find('%') > -1:
                zForm = zFormat[1].replace('|%', '"|%').replace('\s*")', '(\s*"")*)')
            else:
                zForm = zFormat[1].replace('|"\s', '"|"\s').replace('\s*")', '(\s*"")*)')
            answer = "sprintf\s*\(\s*str\s*,\s*\"" + ",".join([nimiX + ":" + xFormat[1], nimiY + ":" + yFormat[1], nimiZ + ":" + zForm]) + "\s*,\s*x\s*,\s*y\s*,\s*z\s*\)\s*;"
        else:
            answer = "sprintf\s*\(\s*str\s*,\s*\"" + ",".join([nimiX + ":" + xFormat[1], nimiY + ":" + yFormat[1], nimiZ + ":" + zFormat[1]]) + "\"\s*,\s*x\s*,\s*y\s*,\s*z\s*\)\s*;"
        raw = {
            "question": question,
            "answer": answer
        }
        return raw, raw

def custom_msgs(question_class, st_code, keywords, constructor, var):
    '''
    - Messages that are shown to the person answering the questions. 
    - Message shown depends if you answer correctly or incorrectly.
    '''
    custom_msgs = core.TranslationDict()
    custom_msgs.set_msg("PrintStudentResult", "fi", "")
    custom_msgs.set_msg("SnippetTest", "fi", "")
    custom_msgs.set_msg("CorrectResult", "fi", "Vastaus oli oikein!")
    custom_msgs.set_msg("IncorrectResult", "fi", "Vastaus oli väärin.")
    custom_msgs.set_msg("fail_variable_value", "fi", "Vastaus oli väärin.")
    custom_msgs.set_msg("GenericErrorMsg", "fi", "Syötettä tarkistettaessa tapahtui virhe.\nVarmista syötteen oikeinkirjoitus.")
    custom_msgs.set_msg("PrintReference", "fi", "")

    custom_msgs.set_msg("PrintStudentResult", "en", "")
    custom_msgs.set_msg("SnippetTest", "en", "")
    custom_msgs.set_msg("CorrectResult", "en", "Correct!")
    custom_msgs.set_msg("IncorrectResult", "en", "Incorrect.")
    custom_msgs.set_msg("fail_variable_value", "en", "Incorrect.")
    custom_msgs.set_msg("GenericErrorMsg", "en", "An error occurred while interpreting your input.  Make sure you didn't make typos.")
    custom_msgs.set_msg("PrintReference", "en", "")
    return custom_msgs

def select_ref(question_class, st_code, keywords, lang):
    '''
    - Creates first reference functions and then a constructor functions in a nested function for
      the different questions.
    - Reference function is variable and value set into an object with setattr function.
    - Constructor function is saved in the variable 'code'.
    - Returns reference function, constructor function and different variables that are used in the
      'custom_msgs' function
    '''
    ref = core.SimpleRef()

    def constructor(st_ans):
        return "a = '" + str(st_ans).strip() + "'"

    setattr(ref, "a", "^\\s*" + keywords["answer"] + "\\s*$")
    return ref, constructor, 0

def validator(ref, res, out):
    """
    Regex validator
    """
    assert re.match(getattr(ref, "a"), getattr(res, "a")), "fail_variable_value"


if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check:
        ref, constructor, var = select_ref( # ref == var
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            args.lang
        )
        constructor_func = constructor(data["answer"])
        msgs = custom_msgs(
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            constructor_func,
            var # == ref
        )
        correct = core.test_code_snippet(
            data["answer"],
            constructor,
            ref, # == var
            args.lang,
            msgs,
            validator=validator
        )
        try: # prevent error from "None/None"
            done, total = [int(x) for x in data["progress"].split("/")]
        except ValueError:
            done, total = 0, 0

        if correct:
            done += 1

        completed = (total - done <= 0)

        data["history"].append([data["question_class"], correct])
        qc, done_temp, total_temp = determine_question(
            data["history"],
            completed,
            args.questions
        )
        if done_temp or total_temp != None:
            done = done_temp
            total = total_temp
        raw, formatdict = generate_params(qc, args.lang)

        out = {
            "question_class": data["question_class"],
            "correct": correct,
            "completed": completed,
            "progress": "{} / {}".format(done, total),
            "next": {
                "question_class": qc,
                "formatdict": formatdict,
                "raw": raw
            }
        }
    else:
        qc, done, total = determine_question(
            data["history"],
            data["completed"],
            args.questions
        )
        #if data["completed"]:
            #done, total = [int(x) for x in data["progress"].split("/")]
        raw, formatdict = generate_params(qc, args.lang)
        out = {
            "question_class": qc,
            "formatdict": formatdict,
            "progress": "{} / {}".format(done, total),
            "correct": False,
            "raw": raw
        }
    core.json_output.wrap_to(out, "log")
