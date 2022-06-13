import json
import random
import test_core as core
from grind_param_library import *

# t1 sijoita arvo 
ASSIGN_VALUE_NUMBER = 0
ASSIGN_VALUE_STRING = 1
# t2 sijoita operaation tulos
ASSIGN_OPERATION = 2
ASSIGN_OPERATION_VARS = 999
# t3 sijoita funktiokutsun tulos
ASSIGN_CALL = 3
# t4 sijoita kaksi arvoa kerralla
ASSIGN_VALUE_MULTIPLE = 4
# t5 sijoita kaksi arvoa funktiokutsusta
ASSIGN_CALL_MULTIPLE = 5
ASSIGN_STRING_MODIFY = 6
ASSIGN_STRING_MODIFY_NO_ARG = 7

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
    if question_class == ASSIGN_VALUE_NUMBER:
        vtype = random.randint(0, 1)
        if vtype == INT_VALUE:
            var_name = random.choice(INT_VAR_NAMES[lang])
            values = random.randint(0, 100)
        elif vtype == FLOAT_VALUE:
            var_name = random.choice(FLOAT_VAR_NAMES[lang])
            values = round(random.random() * 100, 2)
        raw = {
            "var_name": var_name,
            "values": values
        }
        return raw, raw, {}

    elif question_class == ASSIGN_VALUE_STRING:
        vtype = random.randint(2, 3)
        if vtype == NAME_VALUE:
            var_name = random.choice(NAME_VAR_NAMES[lang])
            values = random.choice(RANDOM_NAMES[lang])
        elif vtype == PLACE_VALUE:
            var_name = random.choice(PLACE_VAR_NAMES[lang])
            values = random.choice(RANDOM_PLACES[lang])
        raw = {
            "var_name": var_name,
            "values": values
        }
        formatdict = {
            "var_name": var_name,
            "values": repr(values)
        }
        return raw, formatdict, {}

    elif question_class == ASSIGN_OPERATION:
        op = random.choice("+-/*%")
        if op == "+":
            var_name = random.choice(SUM_VAR_NAMES[lang])
            values = [round(random.random() * 100, 2), round(random.random() * 100, 2)]
        elif op == "-":
            var_name = random.choice(DIF_VAR_NAMES[lang])
            values = [round(random.random() * 100, 2), round(random.random() * 100, 2)]
        elif op == "*":
            var_name = random.choice(MUL_VAR_NAMES[lang])
            values = [round(random.random() * 100, 2), round(random.random() * 100, 2)]
        elif op == "/":
            var_name = random.choice(DIV_VAR_NAMES[lang])
            values = [round(random.random() * 100, 2), round(random.random() * 100 + 0.01, 2)]
        elif op == "%":
            var_name = random.choice(MOD_VAR_NAMES[lang])
            values = [random.randint(0, 100), random.randint(1, 100)]
        raw = {
            "op": op,
            "var_name": var_name,
            "values": values
        }
        formatdict = {
            "op": op,
            "var_name": var_name,
            "values": ", ".join(str(a) for a in values)
        }
        return raw, raw, {}

    elif question_class == ASSIGN_OPERATION_VARS:
        op = random.choice("+-/*%")

    elif question_class == ASSIGN_CALL:
        f = random.choice(SINGLE_RETURN_FUNCTIONS)
        var_name = f.get_rv_name(lang)
        args = f.gen_args(lang)
        raw = {
            "fname": f.name,
            "var_name": var_name,
            "args": args
        }
        formatdict = {
            "fname": f.name,
            "var_name":var_name,
            "args": ", ".join(str(a) for a in args)
        }
        return raw, formatdict, {}

    elif question_class == ASSIGN_VALUE_MULTIPLE:
        n = random.randint(2, 4)
        var_names = []
        values = []
        for i in range(n):
            vtype = random.randint(0, 1)
            if vtype == INT_VALUE:
                var = random.choice(INT_VAR_NAMES[lang])
                while var in var_names:
                    var = random.choice(INT_VAR_NAMES[lang])
                var_names.append(var)
                values.append(random.randint(0, 100))
            elif vtype == FLOAT_VALUE:
                var = random.choice(FLOAT_VAR_NAMES[lang])
                while var in var_names:
                    var = random.choice(FLOAT_VAR_NAMES[lang])
                var_names.append(var)
                values.append(round(random.random() * 100, 2))
        raw = {
            "var_names": var_names,
            "values": values
        }
        formatdict = {
            "var_names": ", ".join(str(a) for a in var_names),
            "values": ", ".join(str(a) for a in values)
        }
        return raw, formatdict, {}

    elif question_class == ASSIGN_CALL_MULTIPLE:
        f = random.choice(MULTI_RETURN_FUNCTIONS)
        var_names = f.get_rv_names(lang)
        args = f.gen_args(lang)
        raw = {
            "fname": f.name,
            "var_names": var_names,
            "args": args
        }
        formatdict = {
            "fname": f.name,
            "var_names": ", ".join(str(a) for a in var_names),
            "args": ", ".join(str(a) for a in args)
        }
        return raw, formatdict, {}

    elif question_class == ASSIGN_STRING_MODIFY:
        f = random.choice([
            StrReplaceMethod, StrLjustMethod, StrRjustMethod, StrZfillMethod
        ])
        name = f.get_rv_name(lang)
        keywords = {
            "fname": f.name,
            "base_var": name,
            "target_var": name,
            "args": f.gen_args(lang)
        }
        meta = {
            "basestr": f.get_str(lang)
        }
        return keywords, meta

    elif question_class == ASSIGN_STRING_MODIFY_NO_ARG:
        f = random.choice([
            StrCapitalizeMethod, StrLowerMethod, StrRstripMethod,
            StrStripMethod, StrTitleMethod, StrUpperMethod
        ])
        name = f.get_rv_name(lang)
        var_names = [name, name]
        keywords = {
            "fname": f.name,
            "var_names": var_names,
        }
        meta = {
            "basestr": f.get_str(lang)
        }
        return keywords, meta

def dummy_constructor(st_code):
    return st_code

def select_ref(question_class, keywords, meta, lang):
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
    if question_class == ASSIGN_VALUE_NUMBER:
        setattr(ref, keywords["var_name"], keywords["values"])
        return ref, dummy_constructor

    elif question_class == ASSIGN_VALUE_STRING:
        setattr(ref, keywords["var_name"], keywords["values"])
        return ref, dummy_constructor

    elif question_class == ASSIGN_OPERATION:
        setattr(ref, keywords["var_name"], eval("{v[0]} {op} {v[1]}".format(
            op=keywords["op"],
            v=keywords["values"]
        )))
        return ref, dummy_constructor

    elif question_class == ASSIGN_CALL:
        setattr(ref, keywords["var_name"], eval(
            keywords["fname"] + "("
            + ", ".join(str(v) for v in keywords["args"])
            + ")"
        ))
        return ref, dummy_constructor

    elif question_class == ASSIGN_OPERATION_VARS:
        pass

    elif question_class == ASSIGN_VALUE_MULTIPLE:
        for var, val in zip(keywords["var_names"], keywords["values"]):
            setattr(ref, var, val)
        return ref, dummy_constructor

    elif question_class == ASSIGN_CALL_MULTIPLE:
        rvs = eval(
            keywords["fname"] + "("
            + ", ".join(str(v) for v in keywords["args"])
            + ")"
        )
        for var, val in zip(keywords["var_names"], rvs):
            setattr(ref, var, val)
        return ref, dummy_constructor

    elif question_class == ASSIGN_STRING_MODIFY:
        pass

    elif question_class == ASSIGN_STRING_MODIFY_NO_ARG:
        pass

if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check: 
        ref, constructor = select_ref(
            data["question_class"],
            data["params"]["raw"],
            data["params"]["meta"],
            args.lang
        )
        correct = core.test_code_snippet(data["answer"], constructor, ref, args.lang)
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
        qc, done, total = determine_question(data["history"], data["completed"], args.questions)
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
