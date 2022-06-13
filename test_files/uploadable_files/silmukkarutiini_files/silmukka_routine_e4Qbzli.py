import json
import random
import sys
import re
import string
import test_core as core
from grind_param_library import *

FOR_BASIC = 0
FOR_BASIC_MULTIVAR = 1
FOR_RANGE = 2
FOR_RANGE_VAR = 3
FOR_ENUMERATE = 4
WHILE_VARIABLE = 5
WHILE_COMPARISON = 6
WHILE_TRUE = 7

sign = {
    "<": "+",
    "<=": "+",
    ">": "-",
    ">=": "-",
    "==": "+",
    "!=": "+"    
}

res_name = {
    "fi": "tulos",
    "en": "result"
}

def highlight_wrap(code):
    code = "{{{{{{highlight=python3\n" + code + "\n}}}}}}"
    return code  

def get_val(op, val):
    '''
    - Generates value for variable.
    - Variable and value is from generate_params function.
    - Value for variable debends on generated value.
    '''
    if op == "<":
        return val / 2
    elif op == "<=":
        return val / 2
    elif op == ">":
        return val * 2
    elif op == ">=":
        return val * 2
    elif op == "==":
        return val
    elif op == "!=":
        return val / 2

def nest_list_sum(aList):
    '''
    Sums elements in a nested list.
    '''
    res = 0 
    for i in aList:
        if isinstance(i, list):
            res += nest_list_sum(i)
        else:
            res += i
    return res

def nest_tuple_sum(aList):
    '''
    Sums elements list of tuples.
    '''
    res = 0 
    for i in aList:
        if isinstance(i, tuple):
            res += nest_tuple_sum(i)
        else:
            res += i
    return res

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

def generate_params(question_class, lang):
    '''
    - Generates all the parameters that are used in the questions. 
    - Returns them as a dictionary.
    - When parameters come in a list it also creates a formated dictionary
      where list is changed into a string.
    '''
    if question_class == FOR_BASIC:
        sequence, loopvar = random.choice(SEQUENCE_PAIR_NAMES[lang])
        raw = {
            "loopvar": loopvar,
            "sequence": sequence
        }
        return raw, raw

    if question_class == FOR_BASIC_MULTIVAR:
        sequence, loopvar = random.choice(SEQUENCE_MULTI_NAMES[lang])
        n = len(loopvar)
        raw = {
            "n": n,
            "loopvar": loopvar,
            "sequence": sequence
        }
        formatdict = {
            "n": n,
            "loopvar": ", ".join(str(a) for a in loopvar),
            "sequence": sequence
        }
        return raw, formatdict

    if question_class == FOR_RANGE:
        n = random.randint(2, 200)
        loopvar = random.choice(INDEX_VAR_NAMES[lang])
        raw = {
            "loopvar": loopvar,
            "n": n
        }
        return raw, raw

    if question_class == FOR_RANGE_VAR:
        loopvar = random.choice(INDEX_VAR_NAMES[lang])
        rangevar = random.choice(RANGE_NAMES[lang])
        raw = {
            "loopvar": loopvar,
            "rangevar": rangevar
        }
        return raw, raw

    if question_class == FOR_ENUMERATE:
        indexvar = random.choice(INDEX_VAR_NAMES[lang])
        sequence, itemvar = random.choice(SEQUENCE_PAIR_NAMES[lang])
        raw = {
            "indexvar": indexvar,
            "itemvar": itemvar,
            "sequence": sequence
        }
        return raw, raw

    if question_class == WHILE_VARIABLE:
        boolean = random.choice([True, False])
        loopvar = random.choice(SEQUENCE_NAMES[lang])
        raw = {
            "loopvar": loopvar,
            "boolean": boolean
        }
        return raw, raw

    if question_class == WHILE_COMPARISON:
        vtype = random.randint(0, 1)
        operation = random.choice(COMP_OPS)
        if vtype == INT_VALUE:
            var = random.choice(INT_VAR_NAMES[lang])
            val = random.randint(0, 100)
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_VAR_NAMES[lang])
            val = round(random.random() * 100, 2)
        raw = {
            "var": var,
            "operation": operation,
            "val": val
        }
        return raw, raw

    if question_class == WHILE_TRUE:
        loopvar = True
        raw = {
            "loopvar": loopvar
        }
        return raw, raw

def custom_msgs(question_class, st_code, keywords, constructor_func, var):
    '''
    - Messages that are shown to the person answering the questions. 
    - Message shown depends if you answer correctly or incorrectly.
    '''
    custom_msgs = core.TranslationDict()
    if question_class == FOR_BASIC:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista muuttujien oikeinkirjoitus,\nsekä että rakennat for-loopin oikein.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{}\n\nChecker constructed and called the function:\n{}\n\nResult in a correct answer:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck variable for typos,\nalso that you build the for-loop correctly.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == FOR_BASIC_MULTIVAR:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista muuttujien oikeinkirjoitus,\nsekä että rakennat for-loopin oikein.")
        custom_msgs.set_msg("PrintReference", "fi", "")
        
        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{}\n\nChecker constructed and called the function:\n{}\n\nResult in a correct answer:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck variable for typos,\nalso that you build the for-loop correctly.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == FOR_RANGE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista muuttujien oikeinkirjoitus,\nsekä että rakennat for-loopin oikein.")
        custom_msgs.set_msg("fail_variable_value", "fi", "Väärä arvo for-loopin range funktiossa.")
        custom_msgs.set_msg("PrintReference", "fi", "")
        
        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{}\n\nChecker constructed and called the function:\n{}\n\nResult in a correct answer:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck variable for typos,\nalso that you build the for-loop correctly.")
        custom_msgs.set_msg("fail_variable_value", "en", "Wrong value in for-loops range function")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == FOR_RANGE_VAR:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista muuttujien oikeinkirjoitus,\nsekä että rakennat for-loopin oikein.")
        custom_msgs.set_msg("fail_variable_value", "fi", "Väärä arvo tai muuttuja for-loopin range funktiossa.")
        custom_msgs.set_msg("PrintReference", "fi", "")
        
        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{}\n\nChecker constructed and called the function:\n{}\n\nResult in a correct answer:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck variable for typos,\nalso that you build the for-loop correctly.")
        custom_msgs.set_msg("fail_variable_value", "en", "Wrong value or variable in for-loops range function")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == FOR_ENUMERATE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista muuttujien oikeinkirjoitus,\nsekä että rakennat for-loopin oikein ja käytit enumerate funktiota.")
        custom_msgs.set_msg("PrintReference", "fi", "")
        
        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{}\n\nChecker constructed and called the function:\n{}\n\nResult in a correct answer:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck variable for typos,\nalso that you build the for-loop correctly and that you used the enumerate function.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == WHILE_VARIABLE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), not keywords["boolean"]))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista muuttujan oikeinkirjoitus,\nsekä että rakennat while-loopin oikein.")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{}\n\nChecker constructed and called the function:\n{}\n\nResult in a correct answer:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck variable for typos,\nalso that you build the while-loop correctly.")
        return custom_msgs

    if question_class == WHILE_COMPARISON:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\nTarkistin rakensi ja kutsui funktion:\n{}\n\nTulos oikeassa vastauksessa:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista muuttujan oikeinkirjoitus,\nsekä että rakennat while-loopin ja ehto lauseen oikein.")
        custom_msgs.set_msg("fail_variable_value", "fi", "Väärä operaattori ehtolauseessa")
        custom_msgs.set_msg("PrintReference", "fi", "")     

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was:\n{}\n\nChecker constructed and called the function:\n{}\n\nResult in a correct answer:\n{}".format(highlight_wrap(st_code), highlight_wrap(constructor_func), var))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck variable for typos,\nalso that you build the while-loop and its condition correctly.")
        custom_msgs.set_msg("fail_variable_value", "en", "Wrong operator in the condition of the while loop.")
        custom_msgs.set_msg("PrintReference", "en", "") 
        return custom_msgs

    if question_class == WHILE_TRUE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "\nVastauksesi oli:\n{}\n\n".format(highlight_wrap(st_code)))
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että rakensit while-silmukan oikein")

        custom_msgs.set_msg("PrintStudentResult", "en", "\nYour answer was::\n{}\n\n".format(highlight_wrap(st_code)))
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you build the while-loop correctly.")
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
    if question_class == FOR_BASIC:
        var = random.sample(range(1,100), 5)
        res = sum(var)
        setattr(ref, res_name[lang], res)

        def constructor(st_code):
            try:
                code = "def func({}):\n".format(keywords["sequence"])
                code += "   {} = 0\n".format(res_name[lang])
                code += "   {}\n".format(st_code)
                code += "       {} += {}\n".format(res_name[lang], keywords["loopvar"])
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = {}\n".format(keywords["sequence"], var)
                code += "{} = func({})".format(res_name[lang], keywords["sequence"])
            except:
                return st_code
            return code
        return ref, constructor, res

    if question_class == FOR_BASIC_MULTIVAR:
        var = []
        res = 0
        loopvar_sum = " + ".join(keywords["loopvar"])
        for i in range(3):
            var.append(random.sample(range(1,100), len(keywords["loopvar"])))
        res = nest_list_sum(var)
        setattr(ref, res_name[lang], res)

        def constructor(st_code):
            try:
                code = "def func({}):\n".format(keywords["sequence"])
                code += "   {} = 0\n".format(res_name[lang])
                code += "   {}\n".format(st_code)
                code += "       {} += {}\n".format(res_name[lang], loopvar_sum)
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = {}\n".format(keywords["sequence"], var)
                code += "{} = func({})".format(res_name[lang], keywords["sequence"])
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == FOR_RANGE:
        res = 0
        for i in range(keywords["n"]):
            res += i
        setattr(ref, res_name[lang], res)

        def constructor(st_code):
            try:
                code = "def func():\n"
                code += "   {} = 0\n".format(res_name[lang])
                code += "   {}\n".format(st_code)
                code += "       {} += {}\n".format(res_name[lang], keywords["loopvar"])
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = func()".format(res_name[lang])
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == FOR_RANGE_VAR:
        var = random.randint(2,200)
        res = 0
        for i in range(var):
            res += i
        setattr(ref, res_name[lang], res)

        def constructor(st_code):
            try:
                code = "def func({}):\n".format(keywords["rangevar"])
                code += "   {} = 0\n".format(res_name[lang])
                code += "   {}\n".format(st_code)
                code += "       {} += {}\n".format(res_name[lang], keywords["loopvar"])
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = func({})".format(res_name[lang], var)
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == FOR_ENUMERATE:
        var = random.sample(range(1,100), 5)
        res = nest_tuple_sum(enumerate(var))
        setattr(ref, res_name[lang], res)

        def constructor(st_code):
            try:
                code = "def func({}):\n".format(keywords["sequence"])
                code += "   {} = 0\n".format(res_name[lang])
                code += "   {}\n".format(st_code)
                code += "       {} += {} + {}\n".format(
                    res_name[lang],
                    keywords["indexvar"],
                    keywords["itemvar"]
                )
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = {}\n".format(keywords["sequence"], var)
                code += "{} = func({})".format(res_name[lang], var)
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == WHILE_VARIABLE:
        false_true_pairs = [
            (0, random.randint(1, 9)),
            ([], [random.randint(1, 9) for i in range(random.randint(3, 5))]),
            ("", random.sample(string.ascii_lower, random.randint(4, 6))),
            (0.0, random.random() * 10 + 0.1)
        ]
        pair = random.choice(false_true_pairs)
    
        setattr(ref, res_name[lang], 10)

        def constructor(st_code):
            try:
                code = "def func({}):\n".format(keywords["loopvar"])
                code += 4 * " " + "n = 0\n"
                code += 4 * " " + "{}\n".format(st_code)
                code += 8 * " " + "if n == 10:"
                code += 12 * " " + "{} = {}".format(
                    keywords["loopvar"],
                    false_true_pairs[keywords["boolean"]]
                )
                code += 8 * " " + "if n == 100:"
                code += 12 * " " + "break"
                code += 8 * " " + "n += 1"
                code += 4 * " " + "return n\n\n"
                code += "{} = func({})".format(res_name[lang], false_true_pairs[not keywords["boolean"]])
                return code
            except:
                return st_code
        return ref, constructor, 0

    if question_class == WHILE_COMPARISON:
        op = keywords["operation"][0]
        var = get_val(op, keywords["val"])
        var_ref = get_val(op, keywords["val"])
        loop = "{}{}{}".format(var_ref, op, keywords["val"])
        while eval(loop):
            if sign[op] == "+":
                var_ref += 1
                loop = "{}{}{}".format(var_ref, op, keywords["val"])
            else:
                var_ref -= 1
                loop = "{}{}{}".format(var_ref, op, keywords["val"])
        setattr(ref, res_name[lang], var_ref)

        def constructor(st_code):
            try:
                code = "def func({}):\n".format(keywords["var"])
                code += "   {}\n".format(st_code)
                code += "       {} {}= 1\n".format(
                    keywords["var"],
                    sign[op]
                )
                code += "   return {}\n\n".format(keywords["var"])
                code += "{} = func({})".format(res_name[lang], var)
                return code
            except:
                return st_code
        return ref, constructor, var

    if question_class == WHILE_TRUE:
        setattr(ref, res_name[lang], 1)

        def constructor(st_code):
            try:
                st_code = " ".join(st_code.split())
                truth = ["True", "1", "not False", "not 0"]
                true = 0
                for i in truth:
                    if i in st_code:
                        true = 1
                        continue

                if ("while" not in st_code) or true == 0:
                    raise Exception
                
                code = "def func():\n"
                code += "   {}\n".format(st_code)
                code += "       return 1\n\n"
                code += "{} = func()".format(res_name[lang])
                return code
            except:
                return st_code
        return ref, constructor, 0


if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check:
        ref, constructor, msg_var = select_ref(
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            args.lang
        )
        constructor_func = constructor(data["answer"])
        correct = core.test_code_snippet(
            data["answer"],
            constructor,
            ref,
            args.lang,
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