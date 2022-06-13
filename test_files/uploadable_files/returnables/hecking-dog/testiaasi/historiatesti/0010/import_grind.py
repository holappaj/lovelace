import json
import random
import sys
from grind_param_library import *

IMPORT_MODULE = 0
IMPORT_MODULE_AS = 1
IMPORT_NAMES_FROM_MODULE = 2
IMPORT_ALL_FROM_MODULE = 3
CALL_MODULE_FUNCTION = 4

templates = {
    "fi": [
        [
            "Kirjoita koodirivi, jolla otat käyttöön {{{{{{{module}}}}}}}-moduulin erillisenä nimiavaruutena.",
            "Kirjoita koodirivi, joka tuo {{{{{{{module}}}}}}}-moduulin ohjelmasi käyttöön.",
        ],
        [
            "Kirjoita koodirivi, jolla otat käyttöön {{{{{{{module}}}}}}}-moduulin ja annat sille aliakseksi {{{{{{{alias}}}}}}}.",
            "Tuo koodiisi {{{{{{{module}}}}}}}-moduuli nimellä {{{{{{{alias}}}}}}}.",
        ],
        [
            "Kirjoita koodirivi, jolla otat {{{{{{{module}}}}}}}-moduulista käyttöön nimet {{{{{{{names}}}}}}}.",
            "Tuo nimet {{{{{{{names}}}}}}} {{{{{{{module}}}}}}}-moduulista oman ohjelmasi nimiavaruuteen.",            
        ],
        [
            "Kirjoita koodirivi, jolla tuot kaikki {{{{{{{module}}}}}}}-moduulin nimet pääohjelmaasi.",
            "Tuo kaikki {{{{{{{module}}}}}}}-moduulin nimet oman ohjelmasi nimiavaruuteen.",
        ],
        [
            "Kirjoita koodirivi, jolla kutsut {{{{{{{module}}}}}}}-moduulin {{{{{{{function}}}}}}}-funktiota argumenteilla {{{{{{{args}}}}}}}, kun oletetaan että koodissa on jo aikaisemmin suoritettu {{{{{{import {module}}}}}}}. Paluuarvo talletetaan muuttujaan {{{{{{{variable}}}}}}}.",
            "Hae muuttujalle {{{{{{{variable}}}}}}} arvo kutsumalla {{{{{{{module}}}}}}}-moduulin {{{{{{{function}}}}}}}-funktiota argumenteilla {{{{{{{args}}}}}}}, kun oletetaan että koodissa on jo aikaisemmin suoritettu {{{{{{import {module}}}}}}}"
        ]
    ],
    "en": [
        [
            "Write a line that brings {{{{{{{module}}}}}}} module in as a separate namespace.",
            "Write a line of code that allows you to use {{{{{{{module}}}}}}} module in your code.",
        ],
        [
            "Write a line that imports {{{{{{{module}}}}}}} and rename it to {{{{{{{alias}}}}}}}.",
            "Bring {{{{{{{module}}}}}}} module to your code with the alias {{{{{{{alias}}}}}}}.",
        ],
        [
            "Write a line that brings the names {{{{{{{names}}}}}}} from {{{{{{{module}}}}}}} module to your program.",
            "Bring the names {{{{{{{names}}}}}}} from {{{{{{{module}}}}}}} to your program's namespace.",            
        ],
        [
            "Write a line that brings all names from {{{{{{{module}}}}}}} to your program.",
            "Bring all names from {{{{{{{module}}}}}}} to your program's namespace.",
        ],
        [
            "Write a line of code that calls {{{{{{{module}}}}}}} module's {{{{{{{function}}}}}}} function with arguments {{{{{{{args}}}}}}}, with the assumption that {{{{{{import {module}}}}}}} has been executed earlier. The return value is assigned to {{{{{{{variable}}}}}}}.",
            "Get a value for {{{{{{{variable}}}}}}} by calling {{{{{{{function}}}}}}} from {{{{{{{module}}}}}}} with arguments {{{{{{{args}}}}}}}, when the module has been imported with {{{{{{import {module}}}}}}}"
        ]
    ]
}

no_arg_variants = {
    "fi": [
        [], # import
        [], # import as
        [], # import names
        [], # import all
        [
            "Kirjoita koodirivi, jolla kutsut {{{{{{{module}}}}}}}-moduulin {{{{{{{function}}}}}}}-funktiota ilman argumentteja, kun oletetaan että koodissa on jo aikaisemmin suoritettu {{{{{{import {module}}}}}}}. Paluuarvo talletetaan muuttujaan {{{{{{{variable}}}}}}}.",
            "Hae muuttujalle {{{{{{{variable}}}}}}} arvo kutsumalla {{{{{{{module}}}}}}}-moduulin {{{{{{{function}}}}}}}-funktiota ilman argumentteja, kun oletetaan että koodissa on jo aikaisemmin suoritettu {{{{{{import {module}}}}}}}."
        ]
    ],
    "en": [
        [], # import
        [], # import as
        [], # import names
        [], # import all
        [
            "Write a line that calls {{{{{{{module}}}}}}} module's {{{{{{{function}}}}}}} function without arguments, when the module has been imported using {{{{{{import {module}}}}}}}. Assign the return value to {{{{{{{variable}}}}}}}.",
            "Get a value for {{{{{{{variable}}}}}}} by calling {{{{{{{function}}}}}}} from {{{{{{{module}}}}}}} without arguments, assuming that {{{{{{import {module}}}}}}} has been executed earlier."
        ]
    ]
}

def generate_params(template_id, template, lang, no_arg_variant="", no_rv_variant=""):
    
    hints = []
    
    if template_id == IMPORT_MODULE:
        module = random.choice(("math", "datetime", "json", "sys", "os", "random", "collections", "time"))
        question = template.format(module=module)
        answer = "import *" + module
        return question, answer
    
    elif template_id == IMPORT_MODULE_AS:
        module, alias = random.choice((("math", "m"), ("numpy", "np"), ("random", "rand"), ("datetime", "dt"), ("time", "t")))
        question = template.format(module=module, alias=alias)
        answer = "import *" + module + " *as *" + alias
        return question, answer
    
    elif template_id == IMPORT_NAMES_FROM_MODULE:
        module = random.choice(MODULES)()
        names = module.get_names()
        question = template.format(module=module.name, names=", ".join(names))
        answer = "from *" + module.name + " *import *" + ", *".join(names)
        return question, answer
    
    elif template_id == IMPORT_ALL_FROM_MODULE:
        module = random.choice(MODULES)()
        question = template.format(module=module.name)
        answer = "from *" + module.name + " *import *\*"
        return question, answer
    
    elif template_id == CALL_MODULE_FUNCTION:
        module = random.choice(CALLABLE_MODULES)()
        fname, args, varname = module.get_function_call(lang)
        if args:
            question = template.format(module=module.name, function=fname, args=", ".join(repr(a) for a in args), variable=varname)
        else:
            question = variant.format(module=module.name, function=fname, variable=varname)
        
        answer = varname + " *= *" + module.name + " *\. *" + fname + " *\(" + " *, *".join(repr(a).translate(RE_TRANS) for a in args) + " *\)"
        answer = "(?:import +" + module.name + " *\n)?" + answer
        return question, answer
    
if __name__ == "__main__":
    
    try:
        lang = sys.argv[1]
        repeats = int(sys.argv[2])
        templates_available = [int(x) for x in sys.argv[3].split(",")]
    except IndexError:
        print("Not enough arguments")
    except ValueError:
        print("Repeats must be integer")
    else:
    
        instances = []
        templates_remaining = templates_available[:]
    
        for i in range(repeats):
    
            template_id = random.choice(templates_remaining)
            templates_remaining.remove(template_id)
            if len(templates_remaining) <= 2:
                templates_remaining = templates_available[:]
            template = random.choice(templates[lang][template_id])
            if no_arg_variants[lang][template_id]:
                variant = random.choice(no_arg_variants[lang][template_id])
            else:
                variant = ""
                
            question, answer = generate_params(template_id, template, lang, variant)
            answer_re = "^\\s*" + answer + "\\s*$"
            colon_hint_re = "^\\s*" + answer.rstrip(":") + "\\s*$"
            instances.append({
                "variables": {"question": question},    
                "answers": [
                    {
                        "correct": True,
                        "answer_str": answer_re,
                        "is_regex": True
                    }, 
                ]
            })
                
        output = {"repeats": instances}
        
        print(json.dumps(output))
