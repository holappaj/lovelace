import json
import random
import test_core as core
from grind_param_library import *

FUNC_DEFINE = 0
FUNC_DEFINE_PARAMS = 1
FUNC_DEFINE_DEFAULTS = 2
FUNC_RETURN = 3
FUNC_RETURN_MULT = 4

f_content = [
    "{} ** 2",
    "{} / {}",
    "{} / ({} ** {})",
    "{} / ({} ** ({}/{}))",
    "{} / ({} ** ({}**{}/{})"
]

arg_sum = [
    "str({})",
    "str({}) + str({})",
    "str({}) + str({}) + str({})",
    "str({}) + str({}) + str({}) + str({})",
    "str({}) + str({}) + str({}) + str({}) + str({})"
]

args_comma = [
    "\"{}\"",
    "\"{}\", \"{}\"",
    "\"{}\", \"{}\", \"{}\"",
    "\"{}\", \"{}\", \"{}\", \"{}\"",
    "\"{}\", \"{}\", \"{}\", \"{}\", \"{}\""
]

res_name = {
    "fi": "tulos",
    "en": "result"
}

def highlight_wrap(code):
    code = "{{{{{{highlight=python3\n" + code + "\n}}}}}}"
    return code  

#Choosing a question
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

#Creating parameters for all the questions.
def generate_params(question_class, lang):
    '''
    - Generates all the parameters that are used in the questions. 
    - Returns them as a dictionary.
    - When parameters come in a list it also creates a formated dictionary
      where list is changed into a string.
    '''
    if question_class == FUNC_DEFINE:
        fname = random.choice(FUNC_NAMES_PARAMLESS[lang])
        raw = {
            "fname": fname
        }
        return raw, raw

    elif question_class == FUNC_DEFINE_PARAMS:
        fnames, params = random.choice(FUNC_NAMES_PARAMS[lang])
        fname = random.choice(fnames)
        pnames = []
        for options, default in params:
            pnames.append(random.choice(options))
        
        raw = {
            "fname": fname,
            "params": pnames
        }
        formatdict = {
            "fname": fname,
            "params": ", ".join(str(a) for a in pnames)
        }
        return raw, formatdict
    
    elif question_class == FUNC_DEFINE_DEFAULTS:
        defaults_names = {
            "fi": "oletusarvo",
            "en": "default value"
        }

        fnames, params = random.choice(FUNC_NAMES_PARAMS[lang])
        fname = random.choice(fnames)
        ppairs = []

        have_defaults = [1] + [random.randint(0, 1) for i in range(len(params) -1)]
        random.shuffle(have_defaults)

        for has_default, param in zip(have_defaults, params):
            pname = random.choice(param[0])
            if has_default:
                ppairs.append([pname, param[1]])
            else:
                ppairs.append([pname, None])
            
        ppairs.sort(key=lambda x: x[1] == None, reverse=True)
        pnames = [p[0] for p in ppairs]
        defaults = []
        for p in ppairs:
            if p[1] is not None:
                defaults.append(p)
                
        raw = {
            "fname": fname,
            "params": pnames,
            "defaults": defaults
        }
        formatdict = {
            "fname": fname,
            "params": ", ".join(str(a) for a in pnames),
            "defaults": ", ".join(
                "{} ({default} {{{{{{#!python3 {}}}}}}})".format(p[0], repr(p[1]), default=defaults_names[lang]) for p in defaults)
        }
        return raw, formatdict

    elif question_class == FUNC_RETURN:
        var = random.choice(INT_VAR_NAMES[lang] + FLOAT_VAR_NAMES[lang])
        raw = {
            "var": var
        }
        return raw, raw
 
    elif question_class == FUNC_RETURN_MULT:
        varnames = random.sample(
            INT_VAR_NAMES[lang] + FLOAT_VAR_NAMES[lang],
            random.randint(2, 4)
        )
        raw = {
            "var": varnames
        }
        formatdict = {
            "var": ", ".join(str(a) for a in varnames)
        }
        return raw, formatdict

#Custom messages for checker
def custom_msgs(question_class, st_code, keywords, constructor_func, var, lang):
    '''
    - Messages that are shown to the person answering the questions. 
    - Message shown depends if you answer correctly or incorrectly.
    '''
    custom_msgs = core.TranslationDict()
    if question_class == FUNC_DEFINE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nMäärittelit funktion:\n{0}\n\nTarkistin rakensi ja kutsui funktiotasi:\n{1}\n\nFunktiokutsu oikein määritellyssä funktiossa:\ntulos = {2}()\n".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["fname"]))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista funktion oikein määrittäminen.\n\nVastauksesi oli:\n{0}\n\nTarkistin yritti rakentaa ja kutsua kunktiotasi:\n{1}\n\nFunktiokutsu oikein määritellyssä funktiossa:\n{2} = {2}()\n".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["fname"]))
        custom_msgs.set_msg("PrintReference", "fi", "")
        
        custom_msgs.set_msg("PrintStudentResult", "en", "You defined the function as:\n\n{0}Checker constructed and called your function:\n{1}\n\nFunction call in correctly defined function:\n{2} = {2}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["fname"]))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured\nYou tried to define the function as:\n{0}\n\nChecker tried to construct and call your function:\n{1}\n\nFunction call in correctly defined function:\n{2} = {2}()\n".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["fname"]))
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == FUNC_DEFINE_PARAMS:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nMäärittelit funktion:\n{0}\n\nTarkistin rakensi ja kutsui funktiotasi:\n{1}\n\nTulos oikein määritetystä funktiosta:\n{2} = {3}\n".format(highlight_wrap(st_code), highlight_wrap(constructor_func), res_name[lang], var))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista funktion oikein määrittäminen ja sen nimen sekä argumenttien oikeinkirjoitus ja lukumäärä.\n\nVastauksesi oli:\n{}\n\nTehtävässä haettu funktion nimi:\n{}\n\nTehtävässä haetut argumentit:\n{}".format(highlight_wrap(st_code), keywords["fname"], (", ").join(keywords["params"])))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nTarkista argumenttien oikea järjestys ja lukumäärä.")
        custom_msgs.set_msg("PrintReference", "fi", "")
        
        custom_msgs.set_msg("PrintStudentResult", "en", "\nYou defined the function as:\n{0}\n\nChecker constructed and called your function:\n{1}\n\nResult in correctly defined function:\n{2} = {3}\n".format(highlight_wrap(st_code), highlight_wrap(constructor_func), res_name[lang], var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you defined the function correctly. Check also that you named the function and arguments correctly and that there are correct amount of arguments.\n\nYour answer was:\n{}\n\nName of the function wanted in the exercise:\n{}\n\nArguments wanted in the exercise:\n{}".format(highlight_wrap(st_code), keywords["fname"], (", ").join(keywords["params"])))
        custom_msgs.set_msg("fail_variable_value", "en", "Check the correct order and number of the arguments.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == FUNC_DEFINE_DEFAULTS:
        custom_msgs.set_msg("PrintStudentResult", "fi",
            "\nMäärittelit funktion:\n"
            "{0}\n\nTarkistin rakensi ja kutsui funktiotasi:"
            "\n{1}\n\n"
            "Muuttujien arvot kutsun jälkeen:"
            "\n{{res}}".format(
                highlight_wrap(st_code),
                highlight_wrap(constructor_func),
            )
        )
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista funktion oikein määrittäminen ja sen, sekä argumenttien nimien oikeinkirjoitus.\nTarkista myös argumenttien oikea lukumäärä, sekä niiden oletusarvot.\n\nVastauksesi oli:\n{0}\n\nTehtävässä haettu funktion nimi:\n{1}\n\nTehtävässä haetut argumentit ja oletusarvot:\n{2}\n{3}".format(highlight_wrap(st_code), keywords["fname"], (", ").join(keywords["params"]), (", ").join(str(x) for x in keywords["defaults"])))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nTarkista argumenttien nimet, oikea järjestys ja lukumäärä")
        #custom_msgs.set_msg("PrintReference", "fi", "")
        
        custom_msgs.set_msg("PrintStudentResult", "en", "\nYou defined the function as:\n{0}\n\nChecker constructed and called your function:\n{1}\n\nResult in correctly defined function:\n{2} = \"{3}\"".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["fname"], var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While exectuing the code, an error occured.\nCheck that you defined the function correctly and check that the function and the arguments are named correctly.\nCheck also that there are correct amount of arguments and check their default values.\n\nYour answer was:\n{0}\n\nName of the function wanted in the exercise:\n{1}\n\nArgumets and their default values wanted in the exercise:\n{2}\n{3}".format(highlight_wrap(st_code), keywords["fname"], (", ").join(keywords["params"]), (", ").join(str(x) for x in keywords["defaults"])))
        custom_msgs.set_msg("fail_variable_value", "en", "\nCheck names of the arguments, their order, default values and that you have .")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == FUNC_RETURN:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{0}\n\nTarkisin rakensi ja kutsui funktiota vastauksestasi:\n{1}\n\nTulos oikeassa vastauksessa:\n{2} = 1".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["var"]))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nTarkista, että palautat oikean muuttujan.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "\nTarkista, että palautat muuttujan oikein.\nVarmista, että \'return\' avainsana ei puutu, sekä palautit oikean muuttujan.")
        custom_msgs.set_msg("fail_missing_variable", "fi", "\nTarkista, että palautat muuttujan oikein.\nVarmista, että \'return\' avainsana ei puutu, sekä palautit oikean muuttujan.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{0}\n\nChecker constructed and called a function from your answer:\n{1}\n\nResult in correct answer:\n{2} = 1".format(highlight_wrap(st_code), highlight_wrap(constructor_func), keywords["var"]))
        custom_msgs.set_msg("fail_variable_value", "en", "\nCheck that you returned the correct variable.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "\nCheck that you returned the variable correctly.\nMake sure that you aren't missing \'return\' statement and that you returned the correct variable")
        custom_msgs.set_msg("fail_missing_variable", "en", "\nCheck that you returned the variable correctly.\nMake sure that you aren't missing \'return\' statement and that you returned the correct variable")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == FUNC_RETURN_MULT:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{0}\n\nTarkisin rakensi funktion ja kutsui sitä:\n{1}\n\nTulos oikeassa vastauksessa:\n{2} = {3}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), st_code.replace("return ",""),var))
        custom_msgs.set_msg("fail_missing_variable", "fi", "\nTarkista, että nimeät muuttujat oikein, niiden lukumäärä ja että palautit ne oikeassa järjestyksessä.\nTarkista myös ettei sinulta puutu \'return\' avainsana.\n\nVastauksesi oli:\n{}\n\nTarkistin rakensi funktion ja kutsui sitä:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("fail_variable_value", "fi", "\nTarkista, että nimeät muuttujat oikein, niiden lukumäärä ja että palautit ne oikeassa järjestyksessä.\nTarkista myös ettei sinulta puutu \'return\' avainsana.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "\nTarkista, että nimeät muuttujat oikein, niiden lukumäärä ja että palautit ne oikeassa järjestyksessä.\nTarkista myös ettei sinulta puutu \'return\' avainsana.\n\nVastauksesi oli:\n{}\n\nTarkistin rakensi funktion ja kutsui sitä:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{0}\n\nChecker constructed and called a function from your answer:\n{1}\n\nResult\nvar = {2}\n\nResult in correct answer:\nvar = {3}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), st_code.replace("return ",""), var))
        custom_msgs.set_msg("fail_missing_variable", "en", "\nCheck that you name the variables correctly and that you return them correctly and in the correct order\nCheck also that you are not missing the return staement")
        custom_msgs.set_msg("fail_variable_value", "en", "\nCheck that you name the variables correctly and that you return them correctly and in the correct order\nCheck also that you are not missing the return staement")
        custom_msgs.set_msg("GenericErrorMsg", "en", "\nCheck that you name the variables correctly and that you return them correctly and in the correct order\nCheck also that you are not missing the return staement")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs


def select_ref(question_class, st_code, keywords, lang):
    '''
    - Creates first reference functions and then a constructor functions in a
    nested function for the different questions.
    - Reference function is variable
    and value set into an object with setattr function.
    - Constructor function is saved in the variable 'code'.
    - Returns reference functin, constructor function and different variables
    that are used in the 'custom_msgs' function
    '''
    ref = core.SimpleRef()
    if question_class == FUNC_DEFINE:
        #reference function
        setattr(ref, res_name[lang], keywords["fname"])

        #constructor function
        def constructor(st_code):
            try:
                code = st_code + "\n"
                code += "   {} = \"{}\"\n".format(res_name[lang], keywords["fname"])
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = {}()".format(res_name[lang], keywords["fname"])

                return code
            except (NameError, IndentationError):
                return st_code

        return ref, constructor, 0

    elif question_class == FUNC_DEFINE_PARAMS:
        #Reference function
        values_list = [random.randint(1,10) for i in range(len(keywords["params"]))]
        values = ", ".join((list(map(str, values_list))))
        result = eval(f_content[len(keywords["params"]) -1 ].format(*values_list))
        setattr(ref, res_name[lang], result)

        #constructor function
        def constructor(st_code):
            try:
                fcon = f_content[len(keywords["params"]) - 1].format(*keywords["params"])
                code = "{}\n".format(st_code)
                code += "   return {}".format(fcon)
                code += "\n\n"
                code += "{} = {}({})\n\n".format(
                    res_name[lang],
                    keywords["fname"],
                    values
                )
                return code
                
            except (SyntaxError, IndentationError, TypeError, NameError):
                return st_code

        return ref, constructor, result

    elif question_class == FUNC_DEFINE_DEFAULTS:
        #Prepearing variables and values for reference and construction function
        defaults_values_list = []
        for default in keywords["defaults"]:
            defaults_values_list.append(default[1])
        defaults_values = "".join((list(map(str, defaults_values_list))))

        if len(keywords["params"]) != len(keywords["defaults"]):
            rang = len(keywords["params"]) - len(keywords["defaults"])
            values_list = [str(random.randint(1,10)) for i in range(rang)]
        else:
            values_list = []
        values = ", ".join((list(map(str, values_list))))

        #reference function
        values_res = "".join(str(x) for x in values_list)
        result = values_res + defaults_values
        setattr(ref, res_name[lang], result)

        #constructor function
        def constructor(st_code):
            try:
                code = st_code + "\n"
                code += "   {} = {}\n".format(
                    res_name[lang],
                    arg_sum[len(keywords["params"]) - 1].format(*keywords["params"])
                )
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = {}({})".format(
                    res_name[lang],
                    keywords["fname"],
                    values
                )
                return code
            except (SyntaxError, IndentationError, TypeError, NameError):
                return st_code

        return ref, constructor, result

    elif question_class == FUNC_RETURN:
        #reference function
        setattr(ref, keywords["var"], "1")
        
        #constructor function
        def constructor(st_code):
            try:
                code = "def func():\n"
                code += "   {} = \"1\"\n".format(keywords["var"])
                code += "   {}\n\n".format(st_code)
                code += "{} = func()".format(keywords["var"])
                return code
            except (NameError, SyntaxError):
                return st_code
        return ref, constructor, 0

    elif question_class == FUNC_RETURN_MULT:
        #reference function
        variables = ", ".join(keywords["var"])
        for var, val in zip(keywords["var"], keywords["var"]):
            setattr(ref, var, val)

        #constructor function
        def constructor(st_code):
            try:
                code = "def func():\n"
                code += "   {} = {}\n".format(
                    variables,
                    args_comma[len(keywords["var"]) - 1].format(*keywords["var"])
                )
                code += "   {}\n\n".format(st_code)
                code += "{} = func()".format(variables)
                return code
            except (NameError, SyntaxError, TypeError, ValueError):
                return st_code
        return ref, constructor, variables


if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check:
        ref, constructor, var = select_ref(
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
            var,
            args.lang
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
        if data["completed"]:
            done, total = [int(x) for x in data["progress"].split("/")]
        raw, formatdict = generate_params(qc, args.lang)
        out = {
            "question_class": qc,
            "formatdict": formatdict,
            "progress": "{} / {}".format(done, total),
            "raw": raw
        }
    core.json_output.wrap_to(out, "log")
    