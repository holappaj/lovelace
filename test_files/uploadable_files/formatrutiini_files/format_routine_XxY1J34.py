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
        
        values = tmpl.get_values()
        
        raw = {
            "tmpl_str": tmpl_str,
            "format_str": rex,
            "names": names,
            "values": values
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "names": ", ".join(str(a) for a in names)
        }
        return raw, formatdict

    if question_class == FORMAT_KEYWORDS:
        tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string()
        template = tmpl.template
        rex = tmpl.get_rex(kws=True)
        kws_names = list(tmpl.get_var_names(kws=True))
        while len(kws_names) != len(set(kws_names)):
            kws_names = list(tmpl.get_var_names(kws=True))
        answer_pairs = []
        for keyword, name in kws_names:
            answer_pairs.append("{} = {}".format(keyword, name))
        raw = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "answer_pairs": answer_pairs,
            "kws_names": kws_names
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "answer_pairs": ", ".join(str(a) for a in answer_pairs),
            "kws_names": ", ".join(str(a) for a in kws_names)
        }
        return raw, formatdict

    if question_class == FORMAT_DECIMALS_SIMPLE:
        tmpl = SimpleFormatTemplate(lang)
        while "__f__" not in tmpl.template:
            tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string()
        template = tmpl.template
        rex = tmpl.get_rex(spec=FLOAT_SPEC)
        names = tmpl.get_var_names()
        while len(names) != len(set(names)):
            names = tmpl.get_var_names()
        float_names, decimals = tmpl.get_float_spec()
        raw = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "names": names,
            "float_names": float_names,
            "decimals": decimals
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "names": ", ".join(str(a) for a in names),
            "float_names": ", ".join(str(a) for a in float_names),
            "decimals": decimals
        }
        return raw, formatdict

    if question_class == FORMAT_DECIMALS_KEYWORDS:
        tmpl = SimpleFormatTemplate(lang, kws=True)
        while "__f__" not in tmpl.template:
            tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string()
        template = tmpl.template
        rex = tmpl.get_rex(kws=True, spec=FLOAT_SPEC)
        kws_names = list(tmpl.get_var_names(kws=True))
        while len(kws_names) != len(set(kws_names)):
            kws_names = list(tmpl.get_var_names(kws=True))
        float_names, decimals = tmpl.get_float_spec()
        answer_pairs = []
        for keyword, name in kws_names:
            answer_pairs.append("{} = {}".format(keyword, name))
        raw = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "answer_pairs": answer_pairs,
            "kws_names": kws_names,
            "float_names": float_names,
            "decimals": decimals
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "answer_pairs": ", ".join(str(a) for a in answer_pairs),
            "kws_names": ", ".join(str(a) for a in kws_names),
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
        rex = tmpl.get_rex(spec=INT_SPEC)
        names = tmpl.get_var_names()
        while len(names) != len(set(names)):
            names = tmpl.get_var_names()
        int_names, minlength = tmpl.get_int_spec()
        raw = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "names": names,
            "int_names": int_names,
            "decimals": minlength
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "names": ", ".join(str(a) for a in names),
            "int_names": ", ".join(str(a) for a in int_names),
            "decimals": minlength
        }
        return raw, formatdict

    if question_class == FORMAT_ZEROFILL_KEYWORDS:
        tmpl = SimpleFormatTemplate(lang, kws=True)
        while "__d__" not in tmpl.template:
            tmpl = SimpleFormatTemplate(lang, kws=True)
        tmpl_str = tmpl.get_string()
        template = tmpl.template
        rex = tmpl.get_rex(kws=True, spec=INT_SPEC) 
        kws_names = list(tmpl.get_var_names(kws=True))
        while len(kws_names) != len(set(kws_names)):
            kws_names = list(tmpl.get_var_names(kws=True))
        int_names, minlength = tmpl.get_int_spec()
        raw = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "kws_names": kws_names,
            "int_names": int_names,
            "decimals": minlength
        }
        formatdict = {
            "tmpl_str": tmpl_str,
            "rex": rex,
            "kws_names": ", ".join(str(a) for a in kws_names),
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
    if question_class == FORMAT_SIMPLE:
        ref = keywords["format_str"].format(*keywords["values"])
        
        def constructor(st_code):
            names = get_names(keywords["names"])

            code = "def func({}):\n".format(names)
            code += "   {}\n".format(st_code)
            code += "func({})".format(res_name[lang], val)
            return code

    return ref, constructor
        
    
    
    
    
    
    
    if question_class == FORMAT_SIMPLE:
        val_list, val, res = prep_ref(
            keywords["rex"],
            random.randint,
            keywords["names"]
        )
        for i in range(len(res)):
            if "{" in res[i]:
                res[i] = res[i].replace("{",str(val_list[i]))
        res = "".join(res)
        setattr(ref, res_name[lang], res)

        #constructor function
        def constructor(st_code):
            try:
                st_code, no_print = prep_code(st_code)
                names = get_names(keywords["names"])

                code = "def func({}):\n".format(names)
                code += "   {} = {}\n".format(res_name[lang], no_print)
                code += "   {}\n".format(st_code)
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = func({})".format(res_name[lang], val)
                return code
            except:
                return st_code
        return ref, constructor, res, val

    if question_class == FORMAT_KEYWORDS:
        val_list, val, res = prep_ref(
            keywords["rex"],
            random.randint,
            keywords["answer_pairs"]
        )
        for i in range(len(res)):
            if "{" in res[i]:
                res[i] = res[i].replace(
                    "{" + keywords["kws_names"][i][0],
                    str(val_list[i])
                )
        res = "".join(res)

        setattr(ref, res_name[lang], res)

        #constructor function
        def constructor(st_code):
            try:
                st_code, no_print = prep_code(st_code)
                names = get_names(keywords["kws_names"], kws=True)
                code = "def func({}):\n".format(names)
                code += "   {} = {}\n".format(res_name[lang], no_print)
                code += "   {}\n".format(st_code)
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = func({})".format(res_name[lang], val)
                return code
            except:
                return st_code
        return ref, constructor, res, val

    if question_class == FORMAT_DECIMALS_SIMPLE:
        val_list, val, res = prep_ref(
            keywords["rex"],
            random.uniform,
            keywords["names"]
        )
        d = keywords["decimals"]
        des = "{:." + str(d) + "f"
        for i in range(len(res)):
            if "{" in res[i]:
                if des in res[i]:
                    res[i] = res[i].replace(des,str(round(val_list[i], d)))
                else:
                    res[i] = res[i].replace("{",str(val_list[i]))
        res = "".join(res)
        res = res.replace("{","")
        setattr(ref, res_name[lang], res)

        #constructor function
        def constructor(st_code):
            try:
                st_code, no_print = prep_code(st_code)
                names = get_names(keywords["names"])

                code = "def func({}):\n".format(names)
                code += "   {} = {}\n".format(res_name[lang], no_print)
                code += "   {}\n".format(st_code)
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = func({})".format(res_name[lang], val)
                return code
            except:
                return st_code
        return ref, constructor, res, val

    if question_class == FORMAT_DECIMALS_KEYWORDS:
        val_list, val, res = prep_ref(
            keywords["rex"],
            random.uniform,
            keywords["answer_pairs"]
        )
        d = keywords["decimals"]
        des = ":." + str(d) + "f"
        keywords_des = []
        for keyword, _ in keywords["kws_names"]:
            keywords_des.append("{}{}".format(keyword, des))
        for i in range(len(res)):
            if "{" in res[i]:
                if des in res[i]:
                    res[i] = res[i].replace(
                        keywords_des[i],
                        str(round(val_list[i], d))
                    )
                else:
                    res[i] = res[i].replace(
                        keywords["kws_names"][i][0],
                        str(val_list[i])
                    )
        res = "".join(res)
        res = res.replace("{","")
        setattr(ref, res_name[lang], res)

        #constructor function
        def constructor(st_code):
            try:
                st_code, no_print = prep_code(st_code)
                names = get_names(keywords["kws_names"], kws=True)

                code = "def func({}):\n".format(names)
                code += "   {} = {}\n".format(res_name[lang], no_print)
                code += "   {}\n".format(st_code)
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = func({})".format(res_name[lang], val)
                return code
            except:
                return st_code
        return ref, constructor, res, val

    if question_class == FORMAT_ZEROFILL_SIMPLE:
        val_list, val, res = prep_ref(
            keywords["rex"],
            random.randint,
            keywords["names"]
        )
        des = "{:>?0" + str(keywords["decimals"]) + "d?"
        for i in range(len(res)):
            if "{" in res[i]:
                if des in res[i]:
                    res[i] = res[i].replace(
                        des,
                        "0" * (keywords["decimals"] - 1) + str(val_list[i])
                    )
                else:
                    res[i] = res[i].replace("{", str(round(val_list[i])))
        res = "".join(res)
        res = res.replace("{","")
        setattr(ref, res_name[lang], res)

        #constructor function
        def constructor(st_code):
            try:
                st_code, no_print = prep_code(st_code)
                names = get_names(keywords["names"])

                code = "def func({}):\n".format(names)
                code += "   {} = {}\n".format(res_name[lang], no_print)
                code += "   {}\n".format(st_code)
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = func({})".format(res_name[lang], val)
                return code
            except:
                return st_code
        return ref, constructor, res, val

    if question_class == FORMAT_ZEROFILL_KEYWORDS:
        val_list, val, res = prep_ref(
            keywords["rex"],
            random.randint,
            keywords["kws_names"]
        )
        min_l = keywords["decimals"]
        des = ":>?0" + str(min_l) + "d?"
        keywords_des = []
        for keyword, _ in keywords["kws_names"]:
            keywords_des.append("{}{}".format(keyword, des))
        for i in range(len(res)):
            if "{" in res[i]:
                if des in res[i]:
                    res[i] = res[i].replace(
                        keywords_des[i],
                        "0" * (min_l - 1) + str(val_list[i])
                    )
                else:
                    res[i] = res[i].replace(
                        "{" + keywords["kws_names"][i][0],
                        str(round(val_list[i]))
                    )
        res = "".join(res)
        res = res.replace("{","")
        setattr(ref, res_name[lang], res)

        #constructor function
        def constructor(st_code):
            try:
                st_code, no_print = prep_code(st_code)
                names = get_names(keywords["kws_names"], kws=True)

                code = "def func({}):\n".format(names)
                code += "   {} = {}\n".format(res_name[lang], no_print)
                code += "   {}\n".format(st_code)
                code += "   return {}\n\n".format(res_name[lang])
                code += "{} = func({})".format(res_name[lang], val)
                return code
            except:
                return st_code
        return ref, constructor, res, val


if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check:
        ref, constructor, msg_var, msg_val = select_ref(
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            args.lang
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
            validator=core.parsed_result_validator
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
        raw, formatdict = generate_params(qc, args.lang)
        out = {
            "question_class": qc,
            "formatdict": formatdict,
            "progress": "{} / {}".format(done, total),
            "raw": raw
        }
    core.json_output.wrap_to(out, "log")