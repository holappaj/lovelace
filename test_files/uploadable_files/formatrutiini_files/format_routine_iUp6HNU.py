import json
import random
import test_core as core
from grind_param_library import *

FORMAT_SIMPLE = 0
FORMAT_KEYWORDS = 1
FORMAT_DECIMALS_SIMPLE = 2
FORMAT_DECIMALS_KEYWORDS = 3
FORMAT_ZEROFILL_SIMPLE = 4
FORMAT_ZEROFILL_KEYWORDS = 5

res_name = {
    "fi": "tuloste",
    "en": "print"
}

msgs = core.TranslationDict()
msgs.set_msg("PrintStudentResult", "fi", "")
msgs.set_msg("PrintStudentResult", "en", "")
msgs.set_msg("PrintStudentOutput", "fi", "Koodin tuloste:\n{{{{{{\n{output}\n}}}}}}")
msgs.set_msg("PrintStudentOutput", "en", "Code output:\n{{{{{{\n{output}\n}}}}}}")
msgs.set_msg("PrintReference", "fi", "Mallituloste:\n{{{{{{\n{ref}\n}}}}}}")
msgs.set_msg("PrintReference", "en", "Reference output:\n{{{{{{\n{ref}\n}}}}}}")



def prep_ref(rex, randfunc, names):
    '''
    Makes some preperations for constructor function.
    - Generates values in a list and a string form
    - Generates result for reference function.
    '''
    rex = rex.replace("*","")
    rex = rex.replace("\\","")
    val_list = [round(randfunc(1,9), 5) for i in range(len(names))]
    val = ", ".join((list(map(str, val_list))))
    res = "{}".format(rex)
    res = res.split("}")
    return val_list, val, res

def prep_code(st_code):
    '''
    Makes some preperations for the code of the person answering the questions.
    - Parses extra white spaces
    - Saves print() functions argument in a variable.
    '''
    st_code = " ".join(st_code.split())
    if ("print(" and "format(") not in st_code:
        raise Exception("Missing print or format")
    no_print = st_code.replace("print(","")
    no_print = no_print.rsplit(")",1)[0]
    return st_code, no_print

def get_names(names_list, kws=False):
    '''
    Turns list of names in to string of names seperated by a comma.
    - kws, means that name is taken from a list where there are name, keyword
      pairs.
    '''
    if kws:
        names = []
        for _, name in names_list:
            names.append(name)
        names = ", ".join(names)
        return names
    else:
        names = ", ".join(names_list)
        return names

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
    if question_class == FORMAT_SIMPLE:
        tmpl = SimpleFormatTemplate(lang)
        tmpl_str = tmpl.get_string()
        rex = tmpl.get_rex(finalize=False)
        template = tmpl.template
        names = tmpl.get_var_names()
        while len(names) != len(set(names)):
            names = tmpl.get_var_names()
        
        values = tmpl.get_var_values()
        
        raw = {
            "tmpl_str": tmpl_str,
            "format_str": rex,
            "names": names,
            "values": values
        }
        
        setup_values = tmpl.get_var_values()
        setup_str = "{{{highlight=python3\n"
        for name, value in zip(names, setup_values):
            setup_str += "{} = {}\n".format(name, value)
        setup_str += "}}}"
        
        formatdict = {
            "tmpl_str": tmpl_str,
            "names": ", ".join(str(a) for a in names),
            "setup": setup_str
        }
        return raw, formatdict

    if question_class == FORMAT_KEYWORDS:
        tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string(kws=True)
        template = tmpl.template
        rex = tmpl.get_rex(kws=True, finalize=False)
        kws_names = list(tmpl.get_var_names(kws=True))
        while len(kws_names) != len(set(kws_names)):
            kws_names = list(tmpl.get_var_names(kws=True))
        
        question_pairs = []
        names = []
        for keyword, name in kws_names:        
            question_pairs.append("{}: {}".format(keyword, name))
            names.append(name)
            
        assignments = {}
        values = tmpl.get_var_values()
        for (keyword, name), value in zip(kws_names, values):
            assignments[keyword] = value
            
        setup_values = tmpl.get_var_values()
        setup_str = "{{{highlight=python3\n"
        for name, value in zip(names, setup_values):
            setup_str += "{} = {}\n".format(name, value)
        setup_str += "}}}"

        raw = {
            "tmpl_str": tmpl_str,
            "format_str": rex,
            "names": names,
            "values": values,
            "assignments": assignments
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "kws_names": ", ".join(question_pairs),
            "setup": setup_str
        }
        return raw, formatdict

    if question_class == FORMAT_DECIMALS_SIMPLE:
        tmpl = SimpleFormatTemplate(lang)
        while "__f__" not in tmpl.template:
            tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string()
        template = tmpl.template
        format_str = tmpl.get_rex(spec=FLOAT_SPEC, finalize=False)
        names = tmpl.get_var_names()
        while len(names) != len(set(names)):
            names = tmpl.get_var_names()
        float_names, decimals = tmpl.get_float_spec()

        values = tmpl.get_var_values()
        setup_values = tmpl.get_var_values()
        setup_str = "{{{highlight=python3\n"
        for name, value in zip(names, setup_values):
            setup_str += "{} = {}\n".format(name, value)
        setup_str += "}}}"

        raw = {
            "tmpl_str": tmpl_str,
            "format_str": format_str,
            "names": names,
            "values": values
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "names": ", ".join(str(a) for a in names),
            "float_names": ", ".join(str(a) for a in float_names),
            "decimals": decimals,
            "setup": setup_str
        }
        return raw, formatdict

    if question_class == FORMAT_DECIMALS_KEYWORDS:
        tmpl = SimpleFormatTemplate(lang, kws=True)
        while "__f__" not in tmpl.template:
            tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string(kws=True)
        template = tmpl.template
        rex = tmpl.get_rex(kws=True, finalize=False, spec=FLOAT_SPEC)
        kws_names = list(tmpl.get_var_names(kws=True))
        while len(kws_names) != len(set(kws_names)):
            kws_names = list(tmpl.get_var_names(kws=True))
        
        float_names, decimals = tmpl.get_float_spec()
        question_pairs = []
        names = []
        for keyword, name in kws_names:        
            question_pairs.append("{}: {}".format(keyword, name))
            names.append(name)
            
        assignments = {}
        values = tmpl.get_var_values()
        for (keyword, name), value in zip(kws_names, values):
            assignments[keyword] = value
            
        setup_values = tmpl.get_var_values()
        setup_str = "{{{highlight=python3\n"
        for name, value in zip(names, setup_values):
            setup_str += "{} = {}\n".format(name, value)
        setup_str += "}}}"

        raw = {
            "tmpl_str": tmpl_str,
            "format_str": rex,
            "names": names,
            "values": values,
            "assignments": assignments
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "kws_names": ", ".join(question_pairs),
            "setup": setup_str,
            "float_names": ", ".join(str(a) for a in float_names),
            "decimals": decimals
        }
        return raw, formatdict

    if question_class == FORMAT_ZEROFILL_SIMPLE:
        tmpl = SimpleFormatTemplate(lang)
        while "__d__" not in tmpl.template:
            tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string()
        template = tmpl.template
        format_str = tmpl.get_rex(spec=INT_SPEC, finalize=False)
        names = tmpl.get_var_names()
        while len(names) != len(set(names)):
            names = tmpl.get_var_names()
        int_names, minlength = tmpl.get_int_spec()

        values = tmpl.get_var_values()
        setup_values = tmpl.get_var_values()
        setup_str = "{{{highlight=python3\n"
        for name, value in zip(names, setup_values):
            setup_str += "{} = {}\n".format(name, value)
        setup_str += "}}}"

        raw = {
            "tmpl_str": tmpl_str,
            "format_str": format_str,
            "names": names,
            "values": values
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "names": ", ".join(str(a) for a in names),
            "int_names": ", ".join(str(a) for a in int_names),
            "decimals": minlength,
            "setup": setup_str
        }
        return raw, formatdict


    if question_class == FORMAT_ZEROFILL_KEYWORDS:
        tmpl = SimpleFormatTemplate(lang, kws=True)
        while "__d__" not in tmpl.template:
            tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string(kws=True)
        template = tmpl.template
        rex = tmpl.get_rex(kws=True, finalize=False, spec=INT_SPEC)
        kws_names = list(tmpl.get_var_names(kws=True))
        while len(kws_names) != len(set(kws_names)):
            kws_names = list(tmpl.get_var_names(kws=True))
        
        int_names, minlength = tmpl.get_int_spec()
        question_pairs = []
        names = []
        for keyword, name in kws_names:        
            question_pairs.append("{}: {}".format(keyword, name))
            names.append(name)
            
        assignments = {}
        values = tmpl.get_var_values()
        for (keyword, name), value in zip(kws_names, values):
            assignments[keyword] = value
            
        setup_values = tmpl.get_var_values()
        setup_str = "{{{highlight=python3\n"
        for name, value in zip(names, setup_values):
            setup_str += "{} = {}\n".format(name, value)
        setup_str += "}}}"

        raw = {
            "tmpl_str": tmpl_str,
            "format_str": rex,
            "names": names,
            "values": values,
            "assignments": assignments
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "kws_names": ", ".join(question_pairs),
            "setup": setup_str,
            "int_names": ", ".join(str(a) for a in int_names),
            "decimals": minlength
        }
        return raw, formatdict

#Custom messages for checker, your answer should have 
def custom_msgs(question_class, st_code, keywords, constructor, var, val):
    '''
    - Messages that are shown to the person answering the questions. 
    - Message shown depends if you answer correctly or incorrectly.
    '''
    custom_msgs = core.TranslationDict()
    names = ""
    try:
        names = [i[1] for i in keywords["kws_names"]]
        names = ", ".join(names)
    except:
        try:
            names = ", ".join(keywords["names"])
        except:
            pass
    
    custom_msgs.set_msg("PrintStudentResult", "fi", "Kun muuttujiin \"{}\" sijoitetaan luvut \"{}\".\nTehtävässä haluttuksi tulosteeksi saadaan:\n{}".format(names, val, var))
    custom_msgs.set_msg("fail_missing_variable", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista oikeinkirjoitus, tulostuksen muotoilulla on merkitys\nvarmista myös että tulostit vastauksen ja käytit format:ia.")
    custom_msgs.set_msg("fail_variable_value", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista oikeinkirjoitus, tulostuksen muotoilulla on merkitys\nvarmista myös että tulostit vastauksen ja käytit format:ia.")
    custom_msgs.set_msg("GenericErrorMsg", "fi", "\nKoodia suorittaessa tapahtui virhe.\nTarkista oikeinkirjoitus, tulostuksen muotoilulla on merkitys\nvarmista myös että tulostit vastauksen ja käytit format:ia.")
    custom_msgs.set_msg("PrintReference", "fi", "")
    custom_msgs.set_msg("PrintStudentOutput", "fi", "")

    custom_msgs.set_msg("PrintStudentResult", "en", "\nWhen variables \"{}\" were defined as \"{}\".Then print wanted in the exercise is:\n{}".format(st_code, constructor, var))
    custom_msgs.set_msg("fail_missing_value", "en", "\nWhile running the code an error occured.\nCheck for typos, your answer should have the same apperreance as shown in the exercise\n and check that you printed the answer and used format.")
    custom_msgs.set_msg("fail_variable_value", "en", "\nWhile running the code an error occured.\nCheck for typos, your answer should have the same apperreance as shown in the exercise\n and check that you printed the answer and used format.")
    custom_msgs.set_msg("GenericErrorMsg", "en", "\nWhile running the code an error occured.\nCheck for typos, your answer should have the same apperreance as shown in the exercise\n and check that you printed the answer and used format.")
    custom_msgs.set_msg("PrintReference", "en", "")
    custom_msgs.set_msg("PrintStudentOutput", "en", "")
    return custom_msgs
        
#Selecting reference function according to which question is asked.
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
    ref = lambda s: keywords["format_str"].format(
        *keywords.get("values", []),
        **keywords.get("assignments", {})
    )
                
    st_tmpl = st_code.replace("\"", "'").split("'")[1]
                
    def constructor(st_code):
        names = get_names(keywords["names"])

        code = "def func({}):\n".format(names)
        code += "   {}\n".format(st_code)
        code += "   test = {}.format({}, {})\n".format(
            repr(t_templ),
            ", ".join(names) + ", " +
            ", ".join("{}={}".format(k, v) for k, v in assignments.items())
        )
            
        code += "func({})".format(", ".join(repr(v) for v in keywords["values"]))
        return code

    return ref, constructor
        
def lenient_validator(ref, res, parsed):
    ref = ref.strip().replace(" ", "").lower()
    parsed = parsed.strip().replace(" ", "").lower()
    assert ref == parsed
        
presenters = {
    "ref_vars": lambda x: x
}
        

if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check:
        ref, constructor = select_ref(
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            args.lang,
        )
        constructor_func = constructor(data["answer"])
        # msgs = custom_msgs(
            # data["question_class"],
            # data["answer"],
            # data["params"]["raw"],
            # constructor_func,
            # msg_var,
            # msg_val
        # )
        correct = core.test_code_snippet(
            data["answer"],
            constructor,
            ref,
            args.lang,
            custom_msgs=msgs,
            presenter=presenters,
            validator=lenient_validator,
            hide_output=False
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