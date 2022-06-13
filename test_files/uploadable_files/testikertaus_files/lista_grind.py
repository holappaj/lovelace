import json
import random
import sys
from grind_param_library import *

LIST_DEFINE = 0
LIST_APPEND = 1
LIST_EXTEND = 2
LIST_SORT = 3
LIST_COPY = 4
LIST_SLICE = 5
LIST_REMOVE = 6
LIST_PRINT_ITEM = 7
LIST_DEFINE_EMPTY = 8

SLICE_END_HINT = {
    "fi": "Loppuindeksi on yhdellä liian pieni - leikkauksessa päätepiste on ensimmäinen indeksi joka ei tule mukaan.",
    "en": "The end index is too small by one - in a slice the end index denotes the first index that will not be included."
}

templates = {
    "fi": [
        [
            "Kirjoita koodirivi, joka määrittelee uuden listan {{{{{{{variable}}}}}}}-muuttujaan ja sisältää alkiot {{{{{{#!python3 {items}}}}}}}.",
            "Luo lista, joka sisältää alkiot {{{{{{#!python3 {items}}}}}}} ja anna sille nimeksi {{{{{{{variable}}}}}}}.",
            "Määrittele uusi lista alkioilla {{{{{{#!python3 {items}}}}}}} ja sijoita se {{{{{{{variable}}}}}}}-muuttujaan.",
        ],
        [
            "Kirjoita koodirivi, joka lisää alkion {{{{{{#!python3 {item}}}}}}} listaan, joka on muuttujassa {{{{{{{variable}}}}}}}."       ,
            "Lisää alkio {{{{{{#!python3 {item}}}}}}} {{{{{{{variable}}}}}}}-listaan.",
            "Koodaa lauseke, jolla lisätään {{{{{{{variable}}}}}}}-listaan alkio {{{{{{#!python3 {item}}}}}}}.",
            
        ],
        [
            "Kirjoita koodirivi, joka lisää kaikki alkiot {{{{{{#!python3 {items}}}}}}} {{{{{{{variable}}}}}}}-muuttujassa olevaan listaan.",            
        ],
        [
            "Kirjoita koodirivi, joka järjestää {{{{{{{variable}}}}}}}-muuttujassa olevan listan oletusjärjestykseen.",
            "Järjestä {{{{{{{variable}}}}}}}-lista oletusjärjestykseen.",
        ],
        [
            "Kirjoita koodirivi, joka luo {{{{{{{var_1}}}}}}}-listasta kopion ja sijoittaa sen muuttujaan {{{{{{{var_2}}}}}}}.",
            "Sijoita {{{{{{{var_1}}}}}}}-listan kopio {{{{{{{var_2}}}}}}}-muuttujaan.",
            "Luo kopio {{{{{{{var_1}}}}}}}-muuttujassa olevasta listasta ja anna sille nimeksi {{{{{{{var_2}}}}}}}.",
        ],
        [
            "Kirjoita koodirivi, joka ottaa {{{{{{{var_1}}}}}}}-muuttujassa olevasta listasta alkiot {i0},...,{i1} (viimeinenkin siis halutaan mukaan!) ja sijoittaa saadun pätkän {{{{{{{var_2}}}}}}}-muuttujaan.",
            "Ota listasta {{{{{{{var_1}}}}}}} leikkaus alkaen {i0}-indeksistä {i1}-indeksiin asti (viimeinen tulee mukaan). Sijoita tämä leikkaus {{{{{{{var_2}}}}}}}-muuttujaan.",
        ],
        [
            "Kirjoita koodirivi, joka poistaa {{{{{{{variable}}}}}}}-listasta {{{{{{#!python3 {item}}}}}}}-alkion.",
            "Listasta {{{{{{{variable}}}}}}} halutaan poistaa alkio {{{{{{#!python3 {item}}}}}}}. Miten teet sen?",
        ],
        [
            "Kirjoita koodirivi, joka tulostaa {{{{{{{variable}}}}}}}-listasta alkion kohdasta {i}.",
            "Tulosta listassa {{{{{{{variable}}}}}}} kohdassa {i} oleva arvo.",
        ],
        [
            "Kirjoita koodirivi, joka määrittelee tyhjän listan ja sijoittaa sen muuttujaan {{{{{{{variable}}}}}}}.",
            "Luo tyhjä lista ja anna sille nimeksi {{{{{{{variable}}}}}}}.",
        ]
    ],
    "en": [
        [
            "Write a line of code that defines a new list into {{{{{{{variable}}}}}}} variable, containing items {{{{{{#!python3 {items}}}}}}}.",
            "Create a list containing {{{{{{#!python3 {items}}}}}}} and name it to {{{{{{{variable}}}}}}}.",
            "Define a new list with {{{{{{#!python3 {items}}}}}}} as items and assign it to {{{{{{{variable}}}}}}}.",
        ],
        [
            "Write a line of code that adds {{{{{{#!python3 {item}}}}}}} to a list in the {{{{{{{variable}}}}}}} variable."       ,
            "Add the {{{{{{#!python3 {item}}}}}}} item to the {{{{{{{variable}}}}}}} list.",
            "Code a statement that adds {{{{{{#!python3 {item}}}}}}} to {{{{{{{variable}}}}}}}.",
            
        ],
        [
            "Write a line of code that adds all of the following {{{{{{#!python3 {items}}}}}}} into a list in the {{{{{{{variable}}}}}}} variable.",            
        ],
        [
            "Write a line of code that sorts the list in the {{{{{{{variable}}}}}}} variable into the default order.",
            "Sort {{{{{{{variable}}}}}}} to the default order.",
        ],
        [
            "Write a line of code that creates a copy of the {{{{{{{var_1}}}}}}} list and assigns it to {{{{{{{var_2}}}}}}}.",
            "Assign a copy of {{{{{{{var_1}}}}}}} to the {{{{{{{var_2}}}}}}} variable.",
            "Create a copy of the list in the {{{{{{{var_1}}}}}}} variable and name it to {{{{{{{var_2}}}}}}}.",
        ],
        [
            "Write a line of code that takes items {i0},...,{i1} (inclusive) from the list in the {{{{{{{var_1}}}}}}} variable and assigns the slice to {{{{{{{var_2}}}}}}}.",
            "Take a slice from {{{{{{{var_1}}}}}}} from index {i0} to {i1} (inclusive). Assign this slice to the {{{{{{{var_2}}}}}}} variable.",
        ],
        [
            "Write a line of code that removes {{{{{{#!python3 {item}}}}}}} from the {{{{{{{variable}}}}}}} list.",
            "{{{{{{#!python3 {item}}}}}}} needs to be removed from {{{{{{{variable}}}}}}}. How would you do it?",
        ],
        [
            "Write a line of code that prints the item from index {i} from the {{{{{{{variable}}}}}}} list.",
            "Print from {{{{{{{variable}}}}}}} the item that's in position {i}.",
        ],
        [
            "Write a line of code that defines an empty list and assigns it to {{{{{{{variable}}}}}}}.",
            "Create an empty list andn name it to {{{{{{{variable}}}}}}}.",
        ]
    
    
    ]
}
        
def generate_params(template_id, template, lang):
    
    hints = []
    
    if template_id == LIST_DEFINE:
        vtype = random.choice((INT_VALUE, FLOAT_VALUE, NAME_VALUE))
        if vtype == INT_VALUE:
            var = random.choice(INT_LIST_NAMES[lang])
            items = [random.randint(0, 100) for i in range(random.randint(2, 4))]
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_LIST_NAMES[lang])
            items = [round(random.random() * 100, 2) for i in range(random.randint(2, 4))]
        elif vtype == NAME_VALUE:
            var = random.choice(NAME_LIST_NAMES[lang])
            items = random.sample(RANDOM_NAMES[lang], random.randint(2, 4))            
            
        question = template.format(variable=var, items=", ".join(repr(i) for i in items))
        answer = var + " *= *" + "\\[ *" + " *, *".join(repr(i).translate(RE_TRANS) for i in items) + " *\\]"
        return question, answer, hints
    
    elif template_id == LIST_APPEND:
        vtype = random.choice((INT_VALUE, FLOAT_VALUE, NAME_VALUE))
        if vtype == INT_VALUE:
            var = random.choice(INT_LIST_NAMES[lang])
            item = random.randint(0, 100)
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_LIST_NAMES[lang])
            item = round(random.random() * 100, 2)
        elif vtype == NAME_VALUE:
            var = random.choice(NAME_LIST_NAMES[lang])
            item = random.choice(RANDOM_NAMES[lang])
            
        question = template.format(variable=var, item=repr(item))
        answer = "{var} *\\. *append *\\( *{item} *\\)".format(var=var, item=repr(item).translate(RE_TRANS))
        return question, answer, hints
    
    elif template_id == LIST_EXTEND:
        vtype = random.choice((INT_VALUE, FLOAT_VALUE, NAME_VALUE))
        if vtype == INT_VALUE:
            var = random.choice(INT_LIST_NAMES[lang])
            items = [random.randint(0, 100) for i in range(random.randint(2, 4))]
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_LIST_NAMES[lang])
            items = [round(random.random() * 100, 2) for i in range(random.randint(2, 4))]
        elif vtype == NAME_VALUE:
            var = random.choice(NAME_LIST_NAMES[lang])
            items = random.sample(RANDOM_NAMES[lang], random.randint(2, 4))            
        
        question = template.format(variable=var, items=", ".join(repr(i) for i in items))
        answer = var + "(?: *\\. *extend *\\( *[\\[\\(] *" + " *, *".join(repr(i).translate(RE_TRANS) for i in items) + " *[\\]\\)] *\\)|" 
        answer += " *\\+= *[\\[\\(]? *" + " *, *".join(repr(i).translate(RE_TRANS) for i in items) + " *[\\]\\)]?)"
        
        return question, answer, hints
                
    elif template_id == LIST_SORT:
        var = random.choice(SEQUENCE_NAMES[lang])
        question = template.format(variable=var)
        answer = "{var} *\\. *sort *\\( *\\)".format(var=var)
        return question, answer, hints
    
    elif template_id == LIST_COPY:
        var_1, var_2 = random.choice(LIST_COPY_NAMES[lang])
        question = template.format(var_1=var_1, var_2=var_2)
        answer = "{var_2} *= *{var_1} *\\[ *: *\\]".format(var_1=var_1, var_2=var_2)
        return question, answer, hints

    elif template_id == LIST_SLICE:
        var_1, var_2 = random.choice(LIST_SLICE_NAMES[lang])
        i0 = random.randint(1, 3)
        i1 = random.randint(i0 + 1, i0 + 5)
        question = template.format(var_1=var_1, var_2=var_2, i0=i0, i1=i1)
        answer = "{var_2} *= *{var_1} *\\[ *{i0} *: *{i1} *\\]".format(var_1=var_1, var_2=var_2, i0=i0, i1=i1+1)
        
        hints.append(("{var_2} *= *{var_1} *\\[ *{i0} *: *{i1} *\\]".format(var_1=var_1, var_2=var_2, i0=i0, i1=i1), SLICE_END_HINT[lang]))
        
        return question, answer, hints
                
    elif template_id == LIST_REMOVE:
        vtype = random.choice((INT_VALUE, FLOAT_VALUE, NAME_VALUE))
        if vtype == INT_VALUE:
            var = random.choice(INT_LIST_NAMES[lang])
            item = random.randint(0, 100)
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_LIST_NAMES[lang])
            item = round(random.random() * 100, 2)
        elif vtype == NAME_VALUE:
            var = random.choice(NAME_LIST_NAMES[lang])
            item = random.choice(RANDOM_NAMES[lang])
            
        question = template.format(variable=var, item=repr(item))
        answer = "{var} *\\. *remove *\\( *{item} *\\)".format(var=var, item=repr(item).translate(RE_TRANS))
        return question, answer, hints

    elif template_id == LIST_PRINT_ITEM:
        var = random.choice(SEQUENCE_NAMES[lang])
        i = random.randint(0, 10)
        question = template.format(variable=var, i=i)
        answer = "print *\\( *{var} *\\[ *{i} *\\] *\\)".format(var=var, i=i)
        return question, answer, hints

    elif template_id == LIST_DEFINE_EMPTY:
        var = random.choice(SEQUENCE_NAMES[lang])        
        question = template.format(variable=var)
        answer = var + " *= *" + "\\[ *\\]"
        return question, answer, hints
        
    
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
            question, answer, hints = generate_params(template_id, template, lang)
            answer_re = "^\\s*" + answer + "\\s*$"
            instance = {
                "variables": {"question": question},    
                "answers": [
                    {
                        "correct": True,
                        "answer_str": answer_re,
                        "is_regex": True
                    }, 
                ]
            }
            for rex, hint in hints:
                hint_re = "^\\s*" + rex + "\\s*$"
                instance["answers"].append({
                    "correct": False,
                    "answer_str": hint_re,
                    "is_regex": True,
                    "hint": hint
                })
                
            instances.append(instance)
                
        output = {"repeats": instances}
        
        print(json.dumps(output))
