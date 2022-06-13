import json
import random
import test_core as core
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

res_name = {
    "fi": "tuloste",
    "en": "print"
}

same_id_name = {
    "fi": "sama_lista",
    "en": "same_list"
}
    
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

def highlight_wrap(code):
    code = "{{{{{{highlight=python3\n" + code + "\n}}}}}}"
    return code

def generate_params(question_class, lang):
    '''
    - Generates all the parameters that are used in the questions. 
    - Returns them as a dictionary.
    - When parameters come in a list it also creates a formated dictionary
      where list is changed into a string.
    '''
    if question_class == LIST_DEFINE:
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
        raw = {
            "var": var,
            "items": items
        }
        formatdict = {
            "var": var,
            "items": ", ".join(repr(a) for a in items)
        }
        return raw, formatdict

    if question_class == LIST_APPEND:
        vtype = random.choice((INT_VALUE, FLOAT_VALUE, NAME_VALUE))
        if vtype == INT_VALUE:
            var = random.choice(INT_LIST_NAMES[lang])
            items = random.randint(0, 100)
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_LIST_NAMES[lang])
            items = round(random.random() * 100, 2)
        elif vtype == NAME_VALUE:
            var = random.choice(NAME_LIST_NAMES[lang])
            items = random.choice(RANDOM_NAMES[lang])
        raw = {
            "var": var,
            "items": items
        }
        return raw, raw

    if question_class == LIST_EXTEND:
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
        raw = {
            "var": var,
            "items": items
        }
        formatdict = {
            "var": var,
            "items": ", ".join(repr(a) for a in items)
        }
        return raw, formatdict

    if question_class == LIST_SORT:
        var = random.choice(SEQUENCE_NAMES[lang])
        raw = {
            "var": var
        }
        return raw, raw

    if question_class == LIST_COPY:
        var_1, var_2 = random.choice(LIST_COPY_NAMES[lang])
        raw = {
            "var_1": var_1,
            "var_2": var_2
        }
        formatdict = {
            "var_1": ", ".join(str(a) for a in var_1),
            "var_2": ", ".join(str(a) for a in var_2)
        }
        return raw, raw

    if question_class == LIST_SLICE:
        var_1, var_2 = random.choice(LIST_SLICE_NAMES[lang])
        i0 = random.randint(1, 3)
        i1 = random.randint(i0 + 1, i0 + 5)
        raw = {
            "var_1": var_1,
            "var_2": var_2,
            "i0": i0,
            "i1": i1
        }
        return raw, raw

    if question_class == LIST_REMOVE:
        vtype = random.choice((INT_VALUE, FLOAT_VALUE, NAME_VALUE))
        if vtype == INT_VALUE:
            var = random.choice(INT_LIST_NAMES[lang])
            items = random.randint(0, 100)
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_LIST_NAMES[lang])
            items = round(random.random() * 100, 2)
        elif vtype == NAME_VALUE:
            var = random.choice(NAME_LIST_NAMES[lang])
            items = random.choice(RANDOM_NAMES[lang])
        raw = {
            "var": var,
            "items": items
        }
        return raw, raw

    if question_class == LIST_PRINT_ITEM:
        var = random.choice(SEQUENCE_NAMES[lang])
        i = random.randint(0, 10)
        raw = {
            "var": var,
            "i": i
        }
        return raw, raw

    if question_class == LIST_DEFINE_EMPTY:
        var = random.choice(SEQUENCE_NAMES[lang])
        raw = {
            "var": var
        }
        return raw, raw

def custom_msgs(question_class, st_code, keywords, constructor, var):
    '''
    - Messages that are shown to the person answering the questions. 
    - Message shown depends if you answer correctly or incorrectly.
    '''
    custom_msgs = core.TranslationDict()
    if question_class == LIST_DEFINE:
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että luot listan oikein.")

        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you tried to create the list correctly.")
        return custom_msgs

    if question_class == LIST_APPEND:
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.\nTarkista, että lisäsit alkiot listaan oikein")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että käsittelet listaa oikein.")

        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you customise the list correctly.")
        return custom_msgs

    if question_class == LIST_EXTEND:
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.\nTarkista, että lisäsit alkiot listaan oikein")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että käsittelet listaa oikein.")

        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you customise the list correctly.")
        return custom_msgs

    if question_class == LIST_SORT:
        custom_msgs.set_msg("PrintStudentResult", "fi", "Lista, jota vastauksesi käytti ja vastauksesi:\n{}\n\nOdotetut muuttujien arvot:\n{} = {}".format(highlight_wrap(constructor), keywords["var"], var))
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että käsittelet listaa oikein.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "List used with your answer and your answer:\n{}\n\nExpected variable and value:\n{} = {}".format(highlight_wrap(constructor), keywords["var"], var))
        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.\.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you customise the list correctly.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == LIST_COPY:
        custom_msgs.set_msg("PrintStudentResult", "fi", "Lista, jota vastauksesi käytti ja vastauksesi:\n{}\n\nOdotetut muuttujien arvot:\n{} = {}".format(highlight_wrap(constructor), keywords["var_2"], var))
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että käsittelet listaa oikein.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "List used with your answer and your answer:\n{}\n\nExpected variable and value:\n{} = {}".format(highlight_wrap(constructor), keywords["var_2"], var))
        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you customise the list correctly.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == LIST_SLICE:
        custom_msgs.set_msg("PrintStudentResult", "fi", "Lista, jota vastauksesi käytti ja vastauksesi:\n{}\n\nOdotetut muuttujien arvot:\n{} = {}".format(highlight_wrap(constructor), keywords["var_2"], var))
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että käsittelet listaa oikein.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "List used with your answer and your answer:\n{}\n\nExpected variable and value:\n{} = {}".format(highlight_wrap(constructor), keywords["var_2"], var))
        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you customise the list correctly.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == LIST_REMOVE:
        custom_msgs.set_msg("PrintStudentOutput", "fi", "")
        custom_msgs.set_msg("PrintStudentResult", "fi", "Lista, jota vastauksesi käytti ja vastauksesi:\n{}\n\nOdotetut muuttujien arvot:\n{} = {}".format(highlight_wrap(constructor), keywords["var"], var))
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että käsittelet listaa oikein.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "List used with your answer and your answer:\n{}\n\nExpected variable and value:\n{} = {}".format(highlight_wrap(constructor), keywords["var"], var))
        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you customise the list correctly.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == LIST_PRINT_ITEM:
        custom_msgs.set_msg("PrintStudentResult", "fi", "Lista, jota vastauksesi käytti ja vastauksesi:\n{}\n\nOdotetut muuttujien arvot:\n{} = {}".format(highlight_wrap(constructor), keywords["var"], var))
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että käsittelet listaa oikein.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "List used with your answer and your answer:\n{}\n\nExpected variable and value:\n{} = {}".format(highlight_wrap(constructor), keywords["var"], var))
        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.\.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you customise the list correctly.")
        custom_msgs.set_msg("PrintReference", "en", "")
        return custom_msgs

    if question_class == LIST_DEFINE_EMPTY:
        custom_msgs.set_msg("PrintStudentResult", "fi", "Lista, jota vastauksesi käytti ja vastauksesi:\n{}\n\nOdotetut muuttujien arvot:\n{} = {}".format(highlight_wrap(constructor), keywords["var"], var))
        custom_msgs.set_msg("fail_missing_variable", "fi", "Koodissa ei luotu pyydettyä listaa.\nTarkista tehtävässä haluttu listan nimi ja alkiot.")
        custom_msgs.set_msg("GenericErrorMsg", "fi", "Koodia suorittaessa tapahtui virhe.\nTarkista, että käsittelet listaa oikein.")
        custom_msgs.set_msg("PrintReference", "fi", "")

        custom_msgs.set_msg("PrintStudentResult", "en", "List used with your answer and your answer:\n{}\n\nExpected variable and value:\n{} = {}".format(highlight_wrap(constructor), keywords["var"], var))
        custom_msgs.set_msg("fail_missing_variable", "en", "Requested list was not generated in the code.\nCheck the lists name and items that are wanted in the assignment.\.")
        custom_msgs.set_msg("GenericErrorMsg", "en", "While executing the code, an error occured.\nCheck that you customise the list correctly.")
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
    if question_class == LIST_DEFINE:
        setattr(ref, keywords["var"], keywords["items"])

        def constructor(st_code):
            return st_code
        return ref, constructor, 0

    if question_class == LIST_APPEND:
        res = []
        res.append(keywords["items"])
        setattr(ref, keywords["var"], res)
        setattr(ref, same_id_name[lang], True)

        def constructor(st_code):
            try:
                code = "{} = []\n".format(keywords["var"])
                code += "_id = id({})\n".format(keywords["var"])
                code += st_code + "\n"
                code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["var"])
                return code
            except:
                return st_code
        return ref, constructor, 0

    if question_class == LIST_EXTEND:
        setattr(ref, keywords["var"], keywords["items"])
        setattr(ref, same_id_name[lang], True)

        def constructor(st_code):
            try:
                code = "{} = []\n".format(keywords["var"])
                code += "_id = id({})\n".format(keywords["var"])
                code += st_code + "\n"
                code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["var"])
                return code
            except:
                return st_code
        return ref, constructor, 0

    if question_class == LIST_SORT:
        var = random.sample(range(1,100), 5)
        res = var[:]
        res.sort()
        setattr(ref, keywords["var"], res)
        setattr(ref, same_id_name[lang], True)

        def constructor(st_code):
            try:
                code = "{} = {}\n".format(keywords["var"], var)
                code += "_id = id({})\n".format(keywords["var"])
                code += st_code + "\n"
                code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["var"])
            except:
                return st_code
        return ref, constructor, res

    if question_class == LIST_COPY:
        var = random.sample(range(1,100), 5)
        res = var[:]
        setattr(ref, keywords["var_2"], res)
        setattr(ref, same_id_name[lang], False)

        def constructor(st_code):
            try:
                code = "{} = {}\n".format(keywords["var_1"], var)
                code += "_id = id({})\n".format(keywords["var"])
                code += st_code + "\n"
                code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["var"])
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == LIST_SLICE:
        var = random.sample(range(1,100), 10)
        res = var[keywords["i0"]:keywords["i1"]]
        setattr(ref, keywords["var_2"], res)

        def constructor(st_code):
            try:
                code = "{} = {}\n".format(keywords["var_1"], var)
                code += st_code
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == LIST_REMOVE:
        if isinstance(keywords["items"], str):
            var = random.sample(RANDOM_NAMES[lang], 5)
            res = var[:]
            var.append(keywords["items"])
        else:
            var = random.sample(range(1,100), 5)
            res = var[:]
            var.append(keywords["items"])
        setattr(ref, keywords["var"], res)

        def constructor(st_code):
            try:
                code = "{} = {}\n".format(keywords["var"], var)
                code += st_code
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == LIST_PRINT_ITEM:
        var = random.sample(range(1,100), 11)
        res = var[keywords["i"]]
        setattr(ref, res_name[lang], res)

        def constructor(st_code):
            try:
                if "print(" not in st_code:
                    raise Exception
                temp = st_code.split("(",1)[1]
                temp = temp.replace(")","")
                code = "{} = {}\n".format(keywords["var"], var)
                code += "{} = {}\n".format(res_name[lang], temp)
                code += st_code
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == LIST_DEFINE_EMPTY:
        setattr(ref, keywords["var"], [])

        def constructor(st_code):
            return st_code
        return ref, constructor, 0


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