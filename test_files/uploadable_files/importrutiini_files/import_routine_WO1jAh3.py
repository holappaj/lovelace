import json
import random
import test_core as core
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
            "Kirjoita koodirivi, jolla otat {{{{{{{mname}}}}}}}-moduulista käyttöön nimet {{{{{{{names}}}}}}}.",
            "Tuo nimet {{{{{{{names}}}}}}} {{{{{{{mname}}}}}}}-moduulista oman ohjelmasi nimiavaruuteen.",            
        ],
        [
            "Kirjoita koodirivi, jolla tuot kaikki {{{{{{{mname}}}}}}}-moduulin nimet pääohjelmaasi.",
            "Tuo kaikki {{{{{{{mname}}}}}}}-moduulin nimet oman ohjelmasi nimiavaruuteen.",
        ],
        [
            "Kirjoita koodirivi, jolla kutsut {{{{{{{mname}}}}}}}-moduulin {{{{{{{fname}}}}}}}-funktiota argumenteilla {{{{{{{args}}}}}}}, kun oletetaan että koodissa on jo aikaisemmin suoritettu {{{{{{import {mname}}}}}}}. Paluuarvo talletetaan muuttujaan {{{{{{{varname}}}}}}}.",
            "Hae muuttujalle {{{{{{{varname}}}}}}} arvo kutsumalla {{{{{{{mname}}}}}}}-moduulin {{{{{{{fname}}}}}}}-funktiota argumenteilla {{{{{{{args}}}}}}}, kun oletetaan että koodissa on jo aikaisemmin suoritettu {{{{{{import {mname}}}}}}}"
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
            "Write a line that brings the names {{{{{{{names}}}}}}} from {{{{{{{mname}}}}}}} module to your program.",
            "Bring the names {{{{{{{names}}}}}}} from {{{{{{{mname}}}}}}} to your program's namespace.",            
        ],
        [
            "Write a line that brings all names from {{{{{{{mname}}}}}}} to your program.",
            "Bring all names from {{{{{{{mname}}}}}}} to your program's namespace.",
        ],
        [
            "Write a line of code that calls {{{{{{{mname}}}}}}} module's {{{{{{{fname}}}}}}} function with arguments {{{{{{{args}}}}}}}, with the assumption that {{{{{{import {mname}}}}}}} has been executed earlier. The return value is assigned to {{{{{{{varname}}}}}}}.",
            "Get a value for {{{{{{{varname}}}}}}} by calling {{{{{{{fname}}}}}}} from {{{{{{{mname}}}}}}} with arguments {{{{{{{args}}}}}}}, when the module has been imported with {{{{{{import {mname}}}}}}}"
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
            "Kirjoita koodirivi, jolla kutsut {{{{{{{mname}}}}}}}-moduulin {{{{{{{fname}}}}}}}-funktiota ilman argumentteja, kun oletetaan että koodissa on jo aikaisemmin suoritettu {{{{{{import {mname}}}}}}}. Paluuarvo talletetaan muuttujaan {{{{{{{varname}}}}}}}.",
            "Hae muuttujalle {{{{{{{varname}}}}}}} arvo kutsumalla {{{{{{{mname}}}}}}}-moduulin {{{{{{{fname}}}}}}}-funktiota ilman argumentteja, kun oletetaan että koodissa on jo aikaisemmin suoritettu {{{{{{import {mname}}}}}}}."
        ]
    ],
    "en": [
        [], # import
        [], # import as
        [], # import names
        [], # import all
        [
            "Write a line that calls {{{{{{{mname}}}}}}} module's {{{{{{{fname}}}}}}} function without arguments, when the module has been imported using {{{{{{import {mname}}}}}}}. Assign the return value to {{{{{{{varname}}}}}}}.",
            "Get a value for {{{{{{{varname}}}}}}} by calling {{{{{{{fname}}}}}}} from {{{{{{{mname}}}}}}} without arguments, assuming that {{{{{{import {mname}}}}}}} has been executed earlier."
        ]
    ]
}

res_name = {
    "fi": "tulos",
    "en": "result"
}

yes_arguments = {
    "fi": "argumenteilla ",
    "en": "with arguments "
}

no_arguments = {
    "fi": "ilman argumentteja",
    "en": "without arguments"
}

def highlight_wrap(code):
    code = "{{{{{{highlight=python3\n" + code + "\n}}}}}}"
    return code

def determine_question(history, completed, active):
    '''
    Determines what and if a question needs to be asked. 
    - Depends on cmd line argument and the amount of correct questions answered.
    '''
    if completed:
        return random.choice(active), None, None

    choices = []
    remaining = 0
    done = 0
    for cq in active:
        correct = history.count([cq, True])
        incorrect = history.count([cq, False])
        done += correct
        if correct < 3 or correct <= incorrect:
            choices.append(cq)
            remaining += max(3 - correct, incorrect - correct)

    return random.choice(choices), done, done + remaining

def custom_msgs(question_class, st_code, keywords, constructor_func, var):
    '''
    - Generates all the parameters that are used in the questions. 
    - Returns them as a dictionary.
    - When parameters come in a list it also creates a formated dictionary
      where list is changed into a string.
    '''
    custom_msgs = core.TranslationDict()
    if question_class == IMPORT_MODULE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTehtävässä haluttu moduuli:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["module"]))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista moduulin nimen oikeinkirjoitus,\nsekä mahdollisesti puuttuva \'import\' avainsana.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour asnwer was:\n{}\n\nChecker build and called a function:\n{}\n\nModule wanted in the exercise:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["module"]))
        custom_msgs.set_msg("fail_variable_value", "en", "\nWhile running the code an error occured.\nCheck module name for typos and possibly missing \'import\' statement.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs
    
    if question_class == IMPORT_MODULE_AS:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTehtävässä haluttu moduuli ja alias:\n{}, {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["module"], keywords["alias"]))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista moduulin ja aliaksen nimien oikeinkirjoitus,\nsekä mahdollisesti puuttuva \'import\' tai \'as\' avainsana.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour asnwer was:\n{}\n\nChecker build and called a function:\n{}\n\nModule and alias wanted in the exercise:\n{}, {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["module"],  keywords["alias"]))
        custom_msgs.set_msg("fail_variable_value", "en", "\nWhile running the code an error occured.\nCheck module's and alias' name for typos and possibly missing \'import\' or \'as\' statement.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs
    
    if question_class ==IMPORT_NAMES_FROM_MODULE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTehtävässä haluttu moduuli ja moduulien nimet:\nModuuli: {}\nModuulin nimet: {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["mname"], var))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista moduulin ja moduulien nimien oikeinkirjoitus,\nsekä mahdollisesti puuttuva \'import\' tai \'as\' avainsana.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour asnwer was:\n{}\n\nChecker build and called a function:\n{}\n\nModule and module names wanted in the exercise:\nModule: {}\nModule names: {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["mname"],  var))
        custom_msgs.set_msg("fail_variable_value", "en", "\nWhile running the code an error occured.\nCheck module and module names for typos and possibly missing \'import\' or \'as\' statement.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs
    
    if question_class ==IMPORT_ALL_FROM_MODULE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTehtävässä haluttu moduuli:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["mname"]))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista moduulin nimen oikeinkirjoitus,\nsekä mahdollisesti puuttuva \'import\' tai \'*\'.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour asnwer was:\n{}\n\nChecker build and called a function:\n{}\n\nModule wanted in the exercise:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["mname"]))
        custom_msgs.set_msg("fail_variable_value", "en", "\nWhile running the code an error occured.\nCheck module name for typos and possibly missing \'import\' statement or \'*\'.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs
            
    if question_class == CALL_MODULE_FUNCTION:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTehtävässä halutut muuttuja, moduuli, funktio, sekä argumentit:\nMuuttuja: {}\nModuuli: {}\nFunktio: {}\nArgumentit: {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["varname"], keywords["mname"], keywords["fname"], var))
        custom_msgs.set_msg("fail_missing_variable", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista muuttujan, moduulin, funktion ja argumenttien oikeinkirjoitus\nsekä muuttujaan oikein sijoittaminen ja moduulin funktion oikein kutsuminen.\n\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTehtävässä halutut muuttuja, moduuli, funktio, sekä argumentit:\nMuuttuja: {}\nModuuli: {}\nFunktio: {}\nArgumentit: {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["varname"], keywords["mname"], keywords["fname"], var))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista muuttujan, moduulin, funktion ja argumenttien oikeinkirjoitus\nsekä muuttujaan oikein sijoittaminen ja moduulin funktion oikein kutsuminen.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista muuttujan, moduulin, funktion ja argumenttien oikeinkirjoitus\nsekä muuttujaan oikein sijoittaminen ja moduulin funktion oikein kutsuminen.\n\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTehtävässä halutut muuttuja, moduuli, funktio, sekä argumentit:\nMuuttuja: {}\nModuuli: {}\nFunktio: {}\nArgumentit: {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["varname"], keywords["mname"], keywords["fname"], var))
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour asnwer was:\n{}\n\nChecker build and called a function:\n{}\n\nVariable, module, function and arguments wanted in the exercise:\nVariable: {}\nModule: {}\nFunction: {}\nArguments: {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["varname"], keywords["mname"], keywords["fname"], var))
        custom_msgs.set_msg("fail_missing_variable", "en", "\nWhile running the code an error occured.\nCheck variable, module, function and arguments for typos and the correct way to assing to variabe and to call modules function.\n\nYour asnwer was:\n{}\n\nChecker build and called a function:\n{}\n\nVariable, module, function and arguments wanted in the exercise:\nVariable: {}\nModule: {}\nFunction: {}\nArguments: {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["varname"], keywords["mname"], keywords["fname"], var))
        custom_msgs.set_msg("fail_variable_value", "en", "\nWhile running the code an error occured.\nCheck variable, module, function and arguments for typos and the correct way to assing to variabe and to call modules function.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "\nWhile running the code an error occured.\nCheck variable, module, function and arguments for typos and the correct way to assing to variabe and to call modules function.\n\nYour asnwer was:\n{}\n\nChecker build and called a function:\n{}\n\nVariable, module, function and arguments wanted in the exercise:\nVariable: {}\nModule: {}\nFunction: {}\nArguments: {}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["varname"], keywords["mname"], keywords["fname"], var))
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

def generate_params(question_class, lang):
    '''
    - Generates all the parameters that are used in the questions. 
    - Returns them as a dictionary.
    - When parameters come in a list it also creates a formated dictionary
      where list is changed into a string.
    '''
    if question_class == IMPORT_MODULE:
        module = random.choice(MODULE_NAMES)
        raw = {
            "module": module
        }
        return raw, raw, {}

    if question_class == IMPORT_MODULE_AS:
        module, alias = random.choice(MODULE_NAMES_AS)
        raw = {
            "module": module,
            "alias": alias
        }
        return raw, raw, {}

    if question_class == IMPORT_NAMES_FROM_MODULE:
        module = random.choice(MODULES)()
        names = module.get_names()
        mname = module.name
        raw = {
            "mname": mname,
            "names": names
        }
        formatdict = {
            "mname": mname,
            "names": ", ".join(str(n) for n in names)
        }
        return raw, formatdict, {}

    if question_class == IMPORT_ALL_FROM_MODULE:
        module = random.choice(MODULES)()
        mname = module.name
        raw = {
            "mname": mname
        }
        return raw, raw, {}

    if question_class == CALL_MODULE_FUNCTION:
        module = random.choice(CALLABLE_MODULES)()
        mname = module.name
        fname, args, varname = module.get_function_call(lang)
        if args != []:
            template_args = yes_arguments[lang] + ", ".join(repr(a) for a in args)
        else:
            template_args = no_arguments[lang]
        raw = {
            "template_args": template_args,
            "varname": varname,
            "mname": mname,
            "fname": fname,
            "args": args 
        }
        formatdict = {
            "template_args": template_args,
            "varname": varname,
            "mname": mname,
            "fname": fname,
            "args": ", ".join(repr(a) for a in args)     
        }
        return raw, formatdict, {}

def select_ref(question_class, keywords, lang):
    ref = core.SimpleRef()
    if question_class == IMPORT_MODULE:
        #Reference function
        setattr(ref, res_name[lang], "import {}".format(keywords["module"]))

        #Constructor functin        
        def constructor(st_code):
            st_code = " ".join(st_code.split())
            code = "def func():\n"
            code += "   {} = \"{}\"\n".format(res_name[lang], st_code)
            code += "   return {}\n\n".format(res_name[lang])
            code += "{} = func()".format(res_name[lang])

            return code
            
        return ref, constructor, 0

    if question_class == IMPORT_MODULE_AS:
        #Reference function
        res = "import {} as {}".format(keywords["module"], keywords["alias"])
        setattr(ref, res_name[lang], res)

        #Constructor functin
        def constructor(st_code):
            st_code = " ".join(st_code.split())
            code = "def func():\n"
            code += "   {} = \"{}\"\n".format(res_name[lang], st_code)
            code += "   return {}\n\n".format(res_name[lang])
            code += "{} = func()".format(res_name[lang])
            return code

        return ref, constructor, 0

    if question_class == IMPORT_NAMES_FROM_MODULE:
        #Reference function
        names = ", ".join(keywords["names"])
        res = "from {} import {}".format(keywords["mname"], names)
        setattr(ref, res_name[lang], res)

        #Constructor functin
        def constructor(st_code):
            st_code = st_code.replace(",",", ").replace(" ,",", ")
            st_code = " ".join(st_code.split())
            code = "def func():\n"
            code += "   {} = \"{}\"\n".format(res_name[lang], st_code)
            code += "   return {}\n\n".format(res_name[lang])
            code += "{} = func()".format(res_name[lang])
            return code

        return ref, constructor, names

    if question_class == IMPORT_ALL_FROM_MODULE:
        #Reference function
        res = "from {} import *".format(keywords["mname"])
        setattr(ref, res_name[lang], res)

        #Constructor functin        
        def constructor(st_code):
            st_code = " ".join(st_code.split())
            code = "def func():\n"
            code += "   {} = \"{}\"\n".format(res_name[lang], st_code)
            code += "   return {}\n\n".format(res_name[lang])
            code += "{} = func()".format(res_name[lang])
            return code
   
        return ref, constructor, 0

    if question_class == CALL_MODULE_FUNCTION:
        #Reference function
        args =", ".join((list(map(str, keywords["args"]))))
        res = "{}.{}({})".format(keywords["mname"], keywords["fname"], args)
        setattr(ref, res_name[lang], res)

        #Constructor functin            
        def constructor(st_code):
            try:
                st_code = st_code.replace(",",", ")
                st_code_split = st_code.split("=")
                st_code = str(st_code_split[1])
                st_code = " ".join(st_code.split())
                code = "def func():\n"
                code += "   {} = \"{}\"\n".format(st_code_split[0], st_code)
                code += "   return {}\n\n".format(st_code_split[0])
                code += "{} = func()".format(keywords["varname"])
                return code
            except IndexError:
                return st_code
        return ref, constructor, args
        
if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check: 
        ref, constructor, var = select_ref(
            data["question_class"],
            data["params"]["raw"],
            args.lang
        )
        constructor_func = constructor(data["answer"])
        msgs = custom_msgs(
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            constructor_func,
            var
        )
        correct = core.test_code_snippet(
            data["answer"],
            constructor,
            ref,
            args.lang,
            msgs
        )
        done, total = [int(x) for x in data["progress"].split("/")]

        if correct:
            done += 1

        if total - done <= 0:
            completed = True
        else:
            completed = False

        data["history"].append([data["question_class"], correct])
        qc, done_temp, total_temp = determine_question(
            data["history"],
            completed,
            args.questions
        )
        if not completed:
            done = done_temp
            total = total_temp
        raw, formatdict, meta = generate_params(qc, args.lang)

        out = {
            "question_class": data["question_class"],
            "correct": correct,
            "completed": completed,
            "progress": "{} / {}".format(done, total),
            "next": {
                "question_class": qc,
                "formatdict": formatdict,
                "meta": meta,
                "raw": raw
            }
        }
    else:
        qc, done, total = determine_question(
            data["history"],
            data["completed"],
            args.questions
        )
        if data["completed"]:
            done, total = [int(x) for x in data["progress"].split("/")]

        raw, formatdict, meta = generate_params(qc, args.lang)

        out = {
            "question_class": qc,
            "formatdict": formatdict,
            "meta": meta,
            "progress": "{} / {}".format(done, total),
            "raw": raw
        }
    core.json_output.wrap_to(out, "log")
    
