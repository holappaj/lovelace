import json
import random
import sys
from grind_param_library import *

# t1 vertailu yhdellä operaattorilla
COMPARISON = 0
# t2 muuttujan arvo
VARIABLE_VALUE = 1
# t3 pituuden vertailu
LEN_COMPARISON = 2
# t4 metodin paluuarvo
M_RETURN_VALUE = 3
# t5 metodin paluuarvon vertailu
M_RETURN_VALUE_EQUALS = 4
# t6 kahden muuttujan vertailu
VARIABLE_COMPARISON = 5
# t7 and/or
COMPOUND = 6
# t8 pelkkä else
PLAIN_ELSE = 7

comp_ops = [
    (">", {"fi": "suurempi", "en": "bigger than"}, "<"), 
    (">=", {"fi": "suurempi tai yhtä suuri", "en": "bigger than or equal to"}, "<="),
    ("==", {"fi": "yhtä suuri", "en": "equal to"}, "=="),
    ("!=", {"fi": "eri suuri", "en": "not equal to"}, "!="), 
    ("<=", {"fi": "pienempi tai yhtä suuri", "en": "smaller than or equal to"}, ">="),
    ("<", {"fi": "pienempi", "en": "smaller than"}, ">")
]

connectors = [
    ("and", {"fi": "ja", "en": "and"}),
    ("or", {"fi": "tai", "en": "or"}),
]

boolean_trans = {
    True: {
        "fi": "tosi",
        "en": "true"
    },
    False: {
        "fi": "epätosi",
        "en": "false"
    }
}
    
no_args = {
    "fi": "-ei argumentteja-",
    "en": "-no arguments-"
}

templates = {
    "fi": [
        [
            "Kirjoita '''{statement}'''-lause, jossa tarkistetaan onko {{{{{{{variable}}}}}}}-muuttujan arvo {operation} kuin {{{{{{#!python3 {value}}}}}}}.",
            "Kirjoita '''{statement}'''-lause, jossa muuttujan {{{{{{{variable}}}}}}} arvoa verrataan arvoon {{{{{{#!python3 {value}}}}}}}. Lause on tosi, jos muuttujan arvo on {operation}.",
        ],
        [
            "Kirjoita '''{statement}'''-lause, joka toteutuu, jos {{{{{{{variable}}}}}}}-muuttujan arvo on {boolean}. Käytä tarvittaessa not-operaattoria - älä käytä vertailuoperaattoreita koska niitä ei tarvita.",
            "Kirjoita '''{statement}'''-lause, jossa tarkistetaan onko {{{{{{{variable}}}}}}}:n arvo {boolean}. Käytä tarvittaessa not-operaattoria - älä käytä vertailuoperaattoreita koska niitä ei tarvita.",
        ],
        [
            "Kirjoita '''{statement}'''-lause, jossa tarkistetaan onko {{{{{{{variable}}}}}}}-muuttujassa olevan arvon pituus {operation} kuin {{{{{{#!python3 {value}}}}}}}.",
            "Kirjoita '''{statement}'''-lause, jossa verrataan {{{{{{{variable}}}}}}}-muuttujan pituutta arvoon {{{{{{#!python3 {value}}}}}}}. Lause toteutuu jos pituus on {operation}.",
        ],
#        [
#            "Kirjoita '''{statement}'''-lause, jossa kutsutaan {function}-funktiota argument(e)illa {arguments}, ja joka toteutuu jos paluuarvo on {operation} kuin {{{{{{#!python3 {value}}}}}}}.",
#        ],
        [
            "Kirjoita '''{statement}'''-lause, jossa kutsutaan {{{{{{{variable}}}}}}}-muuttujassa olevan merkkijonon {{{{{{{method}}}}}}}-metodia näillä argumenteilla: {{{{{{#!python3 {args}}}}}}}. Lause toteutuu jos paluuarvo on {boolean}. Käytä tarvittaessa not-operaattoria - älä käytä vertailuoperaattoreita koska niitä ei tarvita.",
            "Kirjoita '''{statement}'''-lause, jossa tarkistetaan onko {{{{{{{variable}.{method}}}}}}}-kutsun paluuarvo {boolean} argumenteilla {{{{{{#!python3 {args}}}}}}}. Käytä tarvittaessa not-operaattoria - älä käytä vertailuoperaattoreita koska niitä ei tarvita.",
        ],
        [
            "Kirjoita '''{statement}'''-lause, jossa kutsutaan {{{{{{{variable}}}}}}}-muuttujassa olevan merkkijonon {{{{{{{method}}}}}}}-metodia näillä argumenteilla: {{{{{{#!python3 {args}}}}}}}. Lause toteutuu jos metodin paluuarvo on sama kuin {{{{{{#!python3 {value}}}}}}}.",
            "Kirjoita '''{statement}'''-lause, jossa verrataan {{{{{{{variable}.{method}}}}}}}-kutsun paluuarvon yhtäsuuruutta arvon {{{{{{#!python3 {value}}}}}}} kanssa, kun kutsutaan argumenteilla {{{{{{#!python3 {args}}}}}}}.", 
        ],
        [
            "Kirjoita '''{statement}'''-lause, jossa tarkistetaan onko {{{{{{{var_1}}}}}}}-muuttujan arvo {operation} kuin {{{{{{{var_2}}}}}}}-muuttujan arvo",
            "Kirjoita '''{statement}'''-lause, jossa verrataan muuttujia {{{{{{{var_1}}}}}}} ja {{{{{{{var_2}}}}}}}. Lause on tosi, jos {{{{{{{var_1}}}}}}} on {operation}.",
        ],
        [
            "Kirjoita '''{statement}'''-lause, jossa tarkistetaan {clauses[0]} '''{connector}''' {clauses[1]}.",
        ],
        [
            "Kirjoita else-lause.",
        ]
    ],
    "en": [
        [
            "Write an '''{statement}''' statement that checks whether value of {{{{{{{variable}}}}}}} is {operation} {{{{{{#!python3 {value}}}}}}}.",
            "Write an '''{statement}''' statement where the value of {{{{{{{variable}}}}}}} is compared to {{{{{{#!python3 {value}}}}}}}. The statement is fulfilled if the variable is {operation} it.",
        ],
        [
            "Write an '''{statement}''' statement that is fulfilled if the value of {{{{{{{variable}}}}}}} is {boolean}. If needed you can use the not operator but you cannot use comparison operators because you don't need to.",
            "Write an '''{statement}''' that checks whether {{{{{{{variable}}}}}}}'s value if {boolean}. If needed you can use the not operator but you cannot use comparison operators because you don't need to."
        ],
        [
            "Write an '''{statement}''' statement that checks whether the length of {{{{{{{variable}}}}}}} is {operation} {{{{{{#!python3 {value}}}}}}}.",
            "Write an '''{statement}''' statement that compares the length of {{{{{{{variable}}}}}}} to {{{{{{#!python3 {value}}}}}}}. The statement is fulfilled if it's {operation} the value."
        ],
        [
            "Write an '''{statement}''' statement where the {{{{{{{method}}}}}}} method of {{{{{{{variable}}}}}}} is called with the following arguments: {{{{{{#!python3 {args}}}}}}}. The stament is fulfilled if the return value is {boolean}. If needed you can use the not operator but you cannot use comparison operators because you don't need to.",
            "Write an '''{statement}''' statement that checks whether the return value of {{{{{{{variable}}}}}}}.{{{{{{{method}}}}}}} call is {boolean} when using the following arguments: {{{{{{#!python3 {args}}}}}}}. If needed you can use the not operator but you cannot use comparison operators because you don't need to."
        ],
        [
            "Write an '''{statement}''' statement where the {{{{{{{method}}}}}}} method of {{{{{{{variable}}}}}}} is called with the following arguments: {{{{{{#!python3 {args}}}}}}}. The stament is fulfilled if the return value is equal to {{{{{{#!python3 {value}}}}}}}.",
            "Write an '''{statement}''' statement that checks whether the return value of {{{{{{{variable}}}}}}}.{{{{{{{method}}}}}}} call is equal to {{{{{{#!python3 {value}}}}}}} when using the following arguments: {{{{{{#!python3 {args}}}}}}}."
        ],
        [
            "Write an '''{statement}''' statement that checks if the value of {{{{{{{var_1}}}}}}} is {operation} {{{{{{{var_2}}}}}}}.",
            "Write an '''{statement}''' statement that compares the value of {{{{{{{var_1}}}}}}} with the value of {{{{{{{var_2}}}}}}}. The statement is fulfilled if {{{{{{{var_1}}}}}}} is {operation}",
        ],
        [
            "Write an '''{statement}''' that checks {clauses[0]} '''{connector}''' {clauses[1]}.",
        ],
        [
            "Write an else statement."
        ]
    ]
}
        
no_arg_variants = {
    "fi": [
        [], # comparison, not needed
        [], # variable value, not needed
        [], # len, not needed
        [   # method call
            "Kirjoita '''{statement}'''-lause, jossa kutsutaan {{{{{{{variable}}}}}}}-muuttujassa olevan merkkijonon {{{{{{{method}}}}}}}-metodia ilman argumentteja. Lause toteutuu jos paluuarvo on {boolean}. Käytä tarvittaessa not-operaattoria - älä käytä vertailuoperaattoreita.",
            "Kirjoita '''{statement}'''-lause, jossa tarkistetaan onko {{{{{{{variable}.{method}}}}}}}-kutsun paluuarvo {boolean} ilman argumentteja. Käytä tarvittaessa not-operaattoria - älä käytä vertailuoperaattoreita.",
        ],
        [   # method return value
            "Kirjoita '''{statement}'''-lause, jossa kutsutaan {{{{{{{variable}}}}}}}-muuttujassa olevan merkkijonon {{{{{{{method}}}}}}}-metodia ilman argumentteja. Lause toteutuu jos metodin paluuarvo on sama kuin {{{{{{#!python3 {value}}}}}}}.",
            "Kirjoita '''{statement}'''-lause, jossa verrataan {{{{{{{variable}.{method}}}}}}}-kutsun paluuarvon yhtäsuuruutta arvon {{{{{{#!python3 {value}}}}}}} kanssa, kun kutsutaan ilman argumentteja.", 
        ],
        [], # variable comparison, not needed
        [], # compound, not needed
        [], # else, not needed
    ],
    "en": [
        [], # comparison, not needed
        [], # variable value, not needed
        [], # len, not needed
        [   # method call
            "Write an '''{statement}''' statement where the {{{{{{{method}}}}}}} method of {{{{{{{variable}}}}}}} is called without arguments. The stament is fulfilled if the return value is {boolean}. If needed you can use the not operator but you cannot use comparison operators because you don't need to.",
            "Write an '''{statement}''' statement that checks whether the return value of {{{{{{{variable}}}}}}}.{{{{{{{method}}}}}}} call is {boolean} when there are no arguments. If needed you can use the not operator but you cannot use comparison operators because you don't need to."
        ],
        [   # method return value
            "Write an '''{statement}''' statement where the {{{{{{{method}}}}}}} method of {{{{{{{variable}}}}}}} is called without arguments. The stament is fulfilled if the return value is equal to {{{{{{#!python3 {value}}}}}}}.",
            "Write an '''{statement}''' statement that checks whether the return value of {{{{{{{variable}}}}}}}.{{{{{{{method}}}}}}} call is equal to {{{{{{#!python3 {value}}}}}}} when using no arguments."
        ],
        [], # variable comparison, not needed
        [], # compound, not needed
        [], # else, not needed
    ]
}
        
        
compound_templates = {
    "fi": [
        [
            "onko {{{{{{{variable}}}}}}}-muuttujan arvo {operation} kuin {{{{{{#!python3 {value}}}}}}}",
        ],
        [
            "onko {{{{{{{variable}}}}}}}-muuttujan arvo {boolean} (ei vertailuoperaattoreita!)",
        ],
        [
            "onko {{{{{{{variable}}}}}}}-muuttujan pituus {operation} kuin {{{{{{#!python3 {value}}}}}}}",
        ],
        [
            "onko {{{{{{{variable}.{method}}}}}}}-kutsun paluuarvo argumenteilla {{{{{{#!python3 {args}}}}}}} {boolean} (ei vertailuoperaattoreita)",
            "onko {{{{{{{variable}.{method}}}}}}}-kutsun paluuarvo ilman argumentteja {boolean} (ei vertailuoperaattoreita)",            
        ],
        [
            "onko {{{{{{{variable}.{method}}}}}}}-kutsun paluuarvo argumenteilla {{{{{{#!python3 {args}}}}}}} sama kuin {{{{{{#!python3 {value}}}}}}}",
            "onko {{{{{{{variable}.{method}}}}}}}-kutsun paluuarvo ilman argumentteja sama kuin {{{{{{#!python3 {value}}}}}}}",
        ],
        [
            "onko {{{{{{{var_1}}}}}}} {operation} kuin {{{{{{{var_2}}}}}}}"
        ]
    ],
    "en": [
        [
            "is the value of {{{{{{{variable}}}}}}} {operation} {{{{{{#!python3 {value}}}}}}}",
        ],
        [
            "is the value of {{{{{{{variable}}}}}}} {boolean} (no comparison operators)",
        ],
        [
            "it the length of {{{{{{{variable}}}}}}} {operation} {{{{{{#!python3 {value}}}}}}}"
        ],
        [
            "is the return value of {{{{{{{variable}.{method}}}}}}} call {boolean} when using arguments: {{{{{{#!python3 {args}}}}}}} (no comparison operators).",
            "is the return value of {{{{{{{variable}.{method}}}}}}} call {boolean} when using no arguments (no comparison operators)."
        ],
        [
            "is the return value of {{{{{{{variable}.{method}}}}}}} call equal to {{{{{{#!python3 {value}}}}}}} when using arguments: {{{{{{#!python3 {args}}}}}}}.",
            "is the return value of {{{{{{{variable}.{method}}}}}}} call equal to {{{{{{#!python3 {value}}}}}}} when using no arguments."
        ],
        [
            "is {{{{{{{var_1}}}}}}} {operation} {{{{{{{var_2}}}}}}}"
        ]
    ]
}

def generate_params(template_id, template, lang, variant=""):

    statement = random.choice(("if", "elif"))
    
    if template_id == COMPARISON:
        vtype = random.randint(0, 1)
        operation = random.choice(comp_ops)
        if vtype == INT_VALUE:
            var = random.choice(INT_VAR_NAMES[lang])
            value = random.randint(0, 100)
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_VAR_NAMES[lang])
            value = round(random.random() * 100, 2)
            
        question = template.format(statement=statement, variable=var, operation=operation[1][lang], value=value)
        answer = "{stmt} +(?:{var} *{op} *{val}|{val} *{rop} *{var}) *:".format(stmt=statement, var=var, op=operation[0], val=value, rop=operation[2])
        return question, answer            
        
    elif template_id == VARIABLE_VALUE:
        boolean = random.choice([True, False])
        var = random.choice(SEQUENCE_NAMES[lang])
        question = template.format(statement=statement, variable=var, boolean=boolean_trans[boolean][lang])
        if boolean:
            answer = "{stmt} +{var} *:".format(stmt=statement, var=var)
        else:
            answer = "{stmt} +not +{var} *:".format(stmt=statement, var=var)
        return question, answer        
        
    elif template_id == LEN_COMPARISON:
        operation = random.choice(comp_ops)
        atype = random.randint(0, 1)
        var = random.choice(SEQUENCE_NAMES[lang])
        value = random.randint(0, 100)
        question = template.format(statement=statement, variable=var, operation=operation[1][lang], value=value)
        answer = "{stmt} +(?:len *\\( *{var} *\\) *{op} *{val}|{val} *{rop} *len *\\( *{var} *\\)) *: *".format(stmt=statement, var=var, op=operation[0], val=value, rop=operation[2])
        return question, answer
    
    elif template_id == M_RETURN_VALUE:
        m = random.choice(CONDITION_METHODS_BOOL)
        var = random.choice(INPUT_VAR_NAMES[lang])
        args = m.gen_args(lang)
        value = m.gen_comp(lang)
        if args:
            question = template.format(statement=statement, variable=var, method=m.name, args=(", ".join(repr(a) for a in args)), boolean=boolean_trans[value][lang])
        else:
            question = variant.format(statement=statement, variable=var, method=m.name, boolean=boolean_trans[value][lang])
        if value: 
            answer = "{stmt} +{var} *\\. *{m} *\\( *" + " *, *".join(repr(a).translate(RE_TRANS) for a in args) + " *\\) *:"
        else:
            answer = "{stmt} +not +{var} *\\. *{m} *\\( *" + " *, *".join(repr(a).translate(RE_TRANS) for a in args) + " *\\) *:"
        
        answer = answer.format(stmt=statement, var=var, m=m.name)
        return question, answer
    
    elif template_id == M_RETURN_VALUE_EQUALS:
        m = random.choice(CONDITION_METHODS_RV_ARG + CONDITION_METHODS_RV_NOARG)
        var = random.choice(INPUT_VAR_NAMES[lang])
        value = m.gen_comp(lang)
        args = m.gen_args(lang)
        if args:
            question = template.format(statement=statement, variable=var, method=m.name, args=(", ".join(repr(a) for a in args)), value=repr(value))
        else:
            question = variant.format(statement=statement, variable=var, method=m.name, value=repr(value))
        answer = "{stmt} +(?:"
        answer += "{var} *\\. *{m} *\\( *" + ", *".join(repr(a).translate(RE_TRANS) for a in args) + " *\\) *== *{val}|"
        answer += "{val} *== *{var} *\\. *{m} *\\( *" + " *, *".join(repr(a).translate(RE_TRANS) for a in args) + " *\\)) *:"
        
        answer = answer.format(stmt=statement, var=var, m=m.name, val=repr(value).translate(RE_TRANS))
        return question, answer
        
    elif template_id == VARIABLE_COMPARISON:
        var_1, var_2 = random.choice(COMP_PAIR_NAMES[lang])
        operation = random.choice(comp_ops)
        question = template.format(statement=statement, var_1=var_1, var_2=var_2, operation=operation[1][lang])
        answer = "{stmt} +(?:{var_1} *{op} *{var_2}|{var_2} *{rop} *{var_1}) *:".format(stmt=statement, var_1=var_1, op=operation[0], var_2=var_2, rop=operation[2])
        return question, answer           
    
    elif template_id == COMPOUND:
        conn = random.choice(connectors)
        questions = []
        answers = []
        for i in range(2):
            cts = templates_available[:]
            try:
                cts.remove(6)
                cts.remove(7)
            except:
                pass
            ct_id = random.choice(cts)
            ct_t = compound_templates[lang][ct_id][0]
            if ct_id in (3, 4):
                ct_v = compound_templates[lang][ct_id][1]
            else:
                ct_v = ""
            question, answer = generate_params(ct_id, ct_t, lang, ct_v)
            questions.append(question)
            answers.append(answer.split(" +", 1)[1].rstrip(":"))

        question = template.format(statement=statement, clauses=questions, connector=conn[1][lang])
        answer = statement + " +" + answers[0] + " +" + conn[0] + " +" + answers[1] + " *:"
        return question, answer 
        
        
    elif template_id == PLAIN_ELSE:
        answer = "else *:"
        return template, answer
        

colon_hint = {
    "fi": "Kaksoispiste puuttuu lopusta.",
    "en": "Missing colon at the end."
}

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
                templates_remaining = templates_available[:-1]
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
                    {
                        "correct": False,
                        "answer_str": colon_hint_re,
                        "is_regex": True,
                        "hint": colon_hint[lang]
                    }, 
                ]
            })
                
        output = {"repeats": instances}
        
        print(json.dumps(output))
