import json
import random
import sys
import re
import string
import test_core as core
from grind_param_library import *

COMPARISON = 0
VARIABLE_VALUE = 1
LEN_COMPARISON = 2
METHOD_RETURN_VALUE = 3
METHOD_RETURN_VALUE_EQUALS = 4
VARIABLE_COMPARISON = 5
COMPOUND = 6
PLAIN_ELSE = 7

connectors = [
    "and",
    "or",
]

res_name = {
    "fi": "tulos",
    "en": "result"
}

COMP_OPS = [
    (">", {"fi": "suurempi", "en": "bigger than"}, "<"), 
    (">=", {"fi": "suurempi tai yhtä suuri", "en": "bigger than or equal to"}, "<="),
    ("==", {"fi": "yhtä suuri", "en": "equal to"}, "=="),
    ("!=", {"fi": "eri suuri", "en": "not equal to"}, "!="), 
    ("<=", {"fi": "pienempi tai yhtä suuri", "en": "smaller than or equal to"}, ">="),
    ("<", {"fi": "pienempi", "en": "smaller than"}, ">")
]

fcall = {
    "<": "\"a\" * int({} / 2)",
    "<=": "\"a\" * int({} / 2)",
    ">": "\"a\" * int({} * 2)",
    ">=": "\"a\" * int({} * 2)",
    "==": "\"a\" * {}",
    "!=": "\"a\" * int({} * 2)"
}

boolean_fi = {
    True: "tosi",
    False: "epätosi"
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

def gen_var(qc="", val="", operation="", boolean="", mname="", args="", var_2=""):
    '''
    Generates variables for different questions.
    '''
    if qc == COMPARISON:
        return gen_var_val(val, op=operation)
    elif qc == VARIABLE_VALUE:
        if boolean:
            return [
                (random.randint(1, 10), 1),
                (0, 0),
                (random.choice(string.ascii_letters), 1),
                ("", 0),
                ([random.randint(1, 10)], 1),
                ([], 0),
                (None, 0)
            ]
        else:
            return [
                (random.randint(1, 10), 0),
                (0, 1),
                (random.choice(string.ascii_letters), 0),
                ("", 1),
                ([random.randint(1, 10)], 0),
                ([], 1),
                (None, 1)
            ]
        return var
    elif qc == LEN_COMPARISON:
        var = gen_var_len(operation, val)
        return var
    elif qc == METHOD_RETURN_VALUE:
        var = gen_string(
            mname,
            args,
            boolean
        )
        return var
    elif qc == METHOD_RETURN_VALUE_EQUALS:
        var = gen_var_val(
            val,
            mname = mname,
            args = args,
            )
        return var
    elif qc == VARIABLE_COMPARISON:
        val = len("".join(var_2)) * random.randint(2,10)
        var = gen_var_val(val, op=operation)
        return var, val

def elif_st(statement, var):
    '''
    Adds another if statement to constructor function
    when question asks you to write an elif statement.
    '''
    if statement == "elif":
        add = "    if {} == -1:\n".format(var)
        add += "        return -1\n"
        return add
    else:
        add = ""
        return add

def get_val_st(st_code):
    '''
    Gets numbers from students answer.
    '''
    try:
        val_st = [] + re.findall(r'\d+(?:\.\d+)?', st_code)
        return val_st
    except IndexError:
        return st_code

def check_statement(st_statement, statement):
    '''
    Makes sure that student uses the correct statement:
    if or elif
    '''
    if st_statement != statement:
        raise Exception
    
def gen_string(mname, args, boolean):
    '''
    Generates random 5 letter string with arguments at the beginning
    or end of string, depending on what question asks you to answer.
    '''
    if boolean == True:
        if mname == "startswith":
            start = "".join(args)
            end = ""
        elif mname == "endswith":
            start = ""
            end = "".join(args)
    else:
        if mname == "startswith":
            start = ""
            end = "".join(args)
        elif mname == "endswith":
            start = "".join(args)
            end = ""

    ascii_u_l = string.ascii_uppercase + string.ascii_lowercase
    middle = "".join(random.choice(ascii_u_l) for i in range(5))
    rand_string = "{}{}{}".format(start, middle, end)
    return rand_string

def gen_var_val(val, op="", mname="", args="", code=""):
    '''
    - Generates value for variable so that the if-statement is true. 
    - Variables value depends on the operation symbol or name of a method.
    '''
    if op:
        if op == "<":
            return [(val / random.randint(2, 4), 1), (val, 0), (val * random.randint(2, 4), 0)]
        elif op == "<=":
            return [(val / random.randint(2, 4), 1), (val, 1), (val * random.randint(2, 4), 0)]
        elif op == ">":
            return [(val * random.randint(2, 4), 1), (val, 0), (val / random.randint(2, 4), 0)]
        elif op == ">=":
            return [(val * random.randint(2, 4), 1), (val, 1), (val / random.randint(2, 4), 0)]
        elif op == "==":
            return [(val * random.randint(2, 4), 0), (val, 1), (val / random.randint(2, 4), 0)]
        elif op == "!=":
            return [(val * random.randint(2, 4), 1), (val, 0), (val / random.randint(2, 4), 1)]

    if mname:
        if mname == "count":
            val = "".join(val * args)
            return val
        if mname == "replace":
            val = args[0] * 5
            return val
        if mname == "lower":
            val = val.upper()
            return val
        if mname == "rstrip":
            val = val + "   "
            return val
        if mname == "strip":
            val = "     " + val + "     "
            return val
        if mname == "upper":
            val = val.lower()
            return val

def random_string(length):
    return "".join(random.choices(string.ascii_letters, k=length))
            
def gen_var_len(op, val):
    '''
    Generates variable of specific length string depending on value.
    '''
    if op == "<":
        return [
            (random_string(val // random.randint(2, 4)), 1),
            (random_string(val), 0),
            (random_string(val * random.randint(2, 4)), 0)
        ]
    elif op == "<=":
        return [
            (random_string(val // random.randint(2, 4)), 1),
            (random_string(val), 1),
            (random_string(val * random.randint(2, 4)), 0)
        ]
    elif op == ">":
        return [
            (random_string(val // random.randint(2, 4)), 0),
            (random_string(val), 0),
            (random_string(val * random.randint(2, 4)), 1)
        ]
    elif op == ">=":
        return [
            (random_string(val // random.randint(2, 4)), 0),
            (random_string(val), 1),
            (random_string(val * random.randint(2, 4)), 1)
        ]
    elif op == "==":
        return [
            (random_string(val // random.randint(2, 4)), 0),
            (random_string(val), 1),
            (random_string(val * random.randint(2, 4)), 0)
        ]
    elif op == "!=":
        return [
            (random_string(val // random.randint(2, 4)), 1),
            (random_string(val), 0),
            (random_string(val * random.randint(2, 4)), 1)
        ]

def find_st_op(st_code, var, op, val):
    '''
    - Figures out which operation student used. 
    - Needed when variables places can be switched and operation turned around:
      x < y to y > x.
    '''
    space = "{} {} {}".format(var, op[0], val)
    no_space = space.replace(" ","")
    rev_space = "{} {} {}".format(val, op[1], var)
    rev_no_space = rev_space.replace(" ","")
    if space or no_space in st_code:
        st_op = op[0]
        return st_op
    elif rev_scape or rev_no_space in st_code:
        st_op = op[1]
        return st_op
    else:
        raise Exception("Wrong operation type")


def determine_question(history, completed, active):
    '''
    - Determines what and if a question needs to be asked. 
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
    statement = random.choice(("if", "elif"))
    if question_class == COMPARISON:
        vtype = random.randint(0,1)
        operation = random.choice(COMP_OPS)
        if vtype == INT_VALUE:
            var = random.choice(INT_VAR_NAMES[lang])
            val = random.randint(0, 100)
        elif vtype == FLOAT_VALUE:
            var = random.choice(FLOAT_VAR_NAMES[lang])
            val = round(random.random() * 100, 2)
        raw = {
            "statement": statement,
            "var": var,
            "operation": operation,
            "val": val
        }
        formatdict = {
            "statement": statement,
            "var": var,
            "operation": operation[1][lang],
            "val": val
        }
        return raw, formatdict

    if question_class == VARIABLE_VALUE:
        boolean = random.choice([True, False])
        boolean_name = boolean_fi[boolean]
        var = random.choice(SEQUENCE_NAMES[lang])
        raw = {
            "boolean_name": boolean_name,
            "statement": statement,
            "boolean": boolean,
            "var": var
        }
        return raw, raw

    if question_class == LEN_COMPARISON:
        operation = random.choice(COMP_OPS)
        var = random.choice(SEQUENCE_NAMES[lang])
        val = random.randint(2, 100)
        raw = {
            "statement": statement,
            "var": var,
            "operation": operation,
            "val": val
        }
        formatdict = {
            "statement": statement,
            "var": var,
            "operation": operation[1][lang],
            "val": val
        }
        return raw, formatdict

    if question_class == METHOD_RETURN_VALUE:
        method = random.choice(CONDITION_METHODS_BOOL)
        mname = method.name
        var = random.choice(INPUT_VAR_NAMES[lang])
        args = method.gen_args(lang)
        boolean = random.choice([True, False])
        boolean_name = boolean_fi[boolean]
        if args != []:
            template_args = yes_arguments[lang] + ", ".join(repr(a) for a in args)
        else:
            template_args = no_arguments[lang]
        raw = {
            "template_args": template_args,
            "boolean_name": boolean_name,
            "statement": statement,
            "boolean": boolean,
            "var": var,
            "mname": mname,
            "args": args
        }
        formatdict = {
            "template_args": template_args,
            "boolean_name": boolean_name,
            "statement": statement,
            "boolean": boolean,
            "var": var,
            "mname": mname,
            "args": ", ".join(str(a).translate(RE_TRANS) for a in args)
        }
        return raw, formatdict

    if question_class == METHOD_RETURN_VALUE_EQUALS:
        method = random.choice(CONDITION_METHODS_RV_ARG + CONDITION_METHODS_RV_NOARG)
        mname = method.name
        var = random.choice(INPUT_VAR_NAMES[lang])
        val = method.gen_comp(lang)
        args = method.gen_args(lang)
        if args != []:
            template_args = yes_arguments[lang] + ", ".join(repr(a) for a in args)
        else:
            template_args = no_arguments[lang]
        raw = {
            "template_args": template_args,
            "statement": statement,
            "var": var,
            "mname": mname,
            "args": args,
            "val": val
            
        }
        formatdict = {
            "template_args": template_args,
            "statement": statement,
            "var": var,
            "mname": mname,
            "args": ", ".join(str(a) for a in args),
            "val": val
        }
        return raw, formatdict

    if question_class == VARIABLE_COMPARISON:
        var, var_2 = random.choice(COMP_PAIR_NAMES[lang])
        operation = random.choice(COMP_OPS)
        raw = {
            "statement": statement,
            "var": var,
            "operation": operation,
            "var_2": var_2
        }
        return raw, raw

    if question_class == COMPOUND:
        conn = random.choice(connectors)
        rand_qc_1 = random.randint(0,5)
        rand_qc_2 = random.randint(0,5)
        qc_1_dict = {"qc": rand_qc_1}
        qc_2_dict = {"qc": rand_qc_2}
        raw_1, _ = generate_params(rand_qc_1, lang)
        raw_2, _ = generate_params(rand_qc_2, lang)
        raw_2["var"] += "_2" 
        try:                    
            raw_2["var_2"] += "_2"
        except:
            pass
        raw_1 = dict(qc_1_dict, **raw_1)
        raw_2 = dict(qc_2_dict, **raw_2)
        raw_1["conn"] = conn
        del raw_2['statement']
        return raw_1, raw_2

    if question_class == PLAIN_ELSE:
        raw = {}
        return raw, raw

def custom_msgs(question_class, st_code, keywords, constructor_func, var, var_2, lang):
    '''
    - Messages that are shown to the person answering the questions. 
    - Message shown depends if you answer correctly or incorrectly.
    '''
    custom_msgs = core.TranslationDict()
    if question_class == COMPARISON:
        custom_msgs.set_msg("fail_variable_value", "fi", "Väärä muuttujan arvo, tarkista tehtävänanto.")
        custom_msgs.set_msg("fail_variable_value", "en", "Wrong variable's value, check the assignment.")
        return custom_msgs

    if question_class == VARIABLE_VALUE:
        return custom_msgs

    if question_class == LEN_COMPARISON:
        custom_msgs.set_msg("fail_variable_value", "fi", "Väärä arvo, tarkista tehtävänanto.")
        custom_msgs.set_msg("fail_variable_value", "en", "Wrong value, check the assignment.")
        return custom_msgs

    if question_class == METHOD_RETURN_VALUE:
        custom_msgs.set_msg("fail_variable_value", "fi", "Virheellinen ehtolause.\nTarkista tehtävässä haluttu metodi ja metodin argumentti.")
        custom_msgs.set_msg("fail_variable_value", "en", "Incorrect if-statement\nCheck the assignment for wanted method and its argument.")
        return custom_msgs
    
    if question_class == METHOD_RETURN_VALUE_EQUALS:
        custom_msgs.set_msg("fail_variable_value", "fi", "Virheellinen ehtolause.\nTarkista tehtävässä haluttu metodi, metodin argumentti\nja arvo johon metodin funktion tulosta verrataan.")
        custom_msgs.set_msg("fail_variable_value", "en", "Incorrect if-statement\nCheck the assignment for wanted method, its argument\nand value that the methods function is compared to.")
        return custom_msgs

    if question_class == VARIABLE_COMPARISON:
        return custom_msgs

    if question_class == COMPOUND:
        return custom_msgs

    if question_class == PLAIN_ELSE:
        return custom_msgs

        
def statement_constructor(st_code, statement):
    code = 4 * " " + "n = 0" + "\n"
    if statement == "if":
        code += 4 * " " + st_code + "\n"
        code += 8 * " " + "n += 1" + "\n"
    elif statement == "elif":
        code += 4 * " " + "if True:" + "\n"
        code += 8 * " " + "pass" + "\n"
        code += 4 * " " + st_code + "\n"
        code += 8 * " " + "n += 1" + "\n"
        code += 4 * " " + "if False:" + "\n"
        code += 8 * " " + "pass" + "\n"
        code += 4 * " " + st_code + "\n"
        code += 8 * " " + "n += 1" + "\n"
    else:
        code += 4 * " " + "if False:" + "\n"
        code += 8 * " " + "pass" + "\n"
        code += 4 * " " + st_code + "\n"
        code += 8 * " " + "n += 1" + "\n"
    code += 4 * " " + "return n" + "\n"
    return code
        
def select_ref(question_class, st_code, keywords, lang, keywords_2=""):
    '''
    - Creates first reference functions and then a constructor functions in a
    nested function for the different questions.
    - Reference function is variable
    and value set into an object with setattr function.
    - Constructor function is saved in the variable 'code'.
    - Returns reference functin, constructor function and different variables
    that are used in the 'custom_msgs' function
    '''
    

    if question_class == COMPARISON:
        test_vars = gen_var(
            question_class,
            val=keywords["val"],
            operation=keywords["operation"][0]
        )
    elif question_class == VARIABLE_VALUE:
        test_vars = gen_var(
            question_class,
            boolean=keywords["boolean"]
        )
    elif question_class == LEN_COMPARISON:
        test_vars = gen_var(
            question_class,
            val=keywords["val"],
            operation=keywords["operation"][0]
        )
    
    ref = core.SimpleRef()
    for i, (_, expected) in enumerate(test_vars, start=1): 
        setattr(ref, "{}_{}".format(res_name[lang], i), expected)
        
    def constructor(st_code):
        try: 
            code = "def func({}):\n".format(keywords["var"])
            code += statement_constructor(st_code, keywords["statement"])
            for i, (var, _) in enumerate(test_vars, start=1): 
                code += "{} = func({})\n".format("{}_{}".format(res_name[lang], i), repr(var))
            return code
        except:
            return st_code
    
    return ref, constructor


    
    if question_class == LEN_COMPARISON:
        #reference function
        var = gen_var(
            question_class,
            val=keywords["val"],
            operation=keywords["operation"][0]
        )
        var_st = gen_var_len(
            find_st_op(
                st_code, keywords["var"],
                keywords["operation"],
                keywords["val"]
            ),
            keywords["val"]
        )
        res = len(var) + keywords["val"]
        setattr(ref, res_name[lang], res)

        #construction function
        code_split = st_code.split(" ",1)
        st_op = code_split[1].replace(":","")
        st_op = st_op.replace("(","(\"")
        st_op = st_op.replace(")","\")")
        st_statement = code_split[0]
        val_st = get_val_st(st_code)
        if st_statement != keywords["statement"]:
            res_st = 1
        else:
            res_st = round(len(var_st) + int(val_st[0]), 2)

        func_call = fcall[keywords["operation"][0]].format(keywords["val"])
        def constructor(st_code):
            try:
                check_statement(st_statement, keywords["statement"])

                code = "def func({}):\n".format(keywords["var"])
                code += elif_st(keywords["statement"], keywords["var"])
                code += "    {}\n".format(st_code)
                code += "       return len({}) + {}\n".format(keywords["var"], val_st[0])
                code += "    else:\n"
                code += "       return 0\n"
                code += "{} = func({})".format(res_name[lang], func_call)
                return code
            except:
                return st_code
        return ref, constructor, res_st, None, func_call, res

    if question_class == METHOD_RETURN_VALUE:
        #reference function
        setattr(ref, res_name[lang], keywords["boolean"])

        #construction function
        var = gen_var(
            question_class,
            mname=keywords["mname"],
            args=keywords["args"],
            boolean=keywords["boolean"]
        )
        def constructor(st_code):
            try:
                code_split = st_code.split(" ",1)
                st_statement = code_split[0]

                check_statement(st_statement, keywords["statement"])
                code = "def func({}):\n".format(keywords["var"])
                code += elif_st(keywords["statement"], keywords["var"])
                code += "    {}\n".format(st_code)
                code += "        return {}\n".format(keywords["boolean"])
                code += "    else:\n"
                code += "       return {}\n\n".format(not keywords["boolean"])
                code += "{} = func(\"{}\")".format(res_name[lang], var)
                return code
            except:
                return st_code
        return ref, constructor, None, None, var, None

    if question_class == METHOD_RETURN_VALUE_EQUALS:
        #reference function
        if keywords["mname"] == "replace":
            val = keywords["args"][1] * 5
        else:
            val = keywords["val"]
        if isinstance(val, int):
            val = str(val)
        setattr(ref, res_name[lang], val)

        #construction function
        var = gen_var(
            question_class,
            val=keywords["val"],
            mname=keywords["mname"],
            args=keywords["args"],
        )
        def constructor(st_code):
            try:
                return_var = 1 if keywords["mname"] == "replace" else keywords["val"]
                code_split = st_code.split(" ",1)
                st_statement = code_split[0]
                st_if_stat = " = " + code_split[1].replace(":","").split("=",1)[0]
                check_statement(st_statement, keywords["statement"])
                

                code = "def func({}):\n".format(keywords["var"])
                code += elif_st(keywords["statement"], keywords["var"])
                code += "    {}\n".format(st_code)
                code += "       return \"{}\"\n".format(return_var)
                code += "    else:\n"
                code += "       return 0\n\n"
                code += "{} = func(\"{}\")".format(res_name[lang], var)
                return code
            except:
                return st_code
        return ref, constructor, val, None, var, None

    if question_class == VARIABLE_COMPARISON:
        #reference function
        var, val = gen_var(
            question_class,
            operation=keywords["operation"][0],
            var_2=keywords["var_2"]
        )
        res = round(var + val, 2)
        setattr(ref, res_name[lang], res)

        #construction function
        def constructor(st_code):
            try:
                code_split = st_code.split(" ",1)
                st_statement = code_split[0]
                check_statement(st_statement, keywords["statement"])
                code = "def func({}, {}):\n".format(
                    keywords["var"],
                    keywords["var_2"]
                )
                code += elif_st(keywords["statement"], keywords["var"])
                code += "    {}\n".format(st_code)
                code += "       return round({} + {}, 2)\n".format(var, val)
                code += "    else:\n"
                code += "       return 1\n\n"
                code += "{} = func({}, {})".format(res_name[lang], var, val)
                return code
            except:
                return st_code
        return ref, constructor, res, val, var, 0
    
    if question_class == COMPOUND:
        #reference function
        setattr(ref, res_name[lang], 1)

        #construction function
        def constructor(st_code):
            keywords_2["statement"] = keywords["statement"]
            qc_1, qc_2 = keywords["qc"], keywords_2["qc"]
            _, _, _, val, var, _ = select_ref(qc_1, st_code, keywords, lang)
            _, _, _, val_2, var_2, _ = select_ref(qc_2, st_code, keywords_2, lang)

            if isinstance(var, str) and qc_1 != LEN_COMPARISON:
                var = "\"{}\"".format(var)
            if isinstance(var_2, str) and qc_2 != LEN_COMPARISON:
                var_2 = "\"{}\"".format(var_2)
            if keywords["conn"] not in st_code:
                    return st_code

            #Checking student code for errors
            try:
                keywords["val"]
                keywords_2["val"]
            except KeyError:
                pass
            else:
                if str(keywords["val"]) not in st_code:
                    return st_code
                if str(keywords_2["val"]) not in st_code:
                    return st_code
            try:
                keywords_2["val"]
            except KeyError:
                pass
            else:
                if str(keywords_2["val"]) not in st_code:
                    return st_code

            if (qc_1 or qc_2) == LEN_COMPARISON:
                if "len(" not in st_code:
                    return st_code
            code_split = st_code.split(" ",1)
            st_statement = code_split[0]     
            check_statement(st_statement, keywords["statement"])

            #Creating funcion call and def, depending on the number of 
            #variables that are called
            variables = []
            variables.append(keywords["var"])
            try:
                variables.append(keywords["var_2"])
            except:
                pass
            variables.append(keywords_2["var"])
            try:
                variables.append(keywords_2["var_2"])
            except:
                pass 

            value = []
            if var is not None:
                value.append(var)
            try:
                if val is not None:
                    value.append(val)
            except:
                pass
            if var_2 is not None:
                value.append(var_2)
            try:
                if val_2 is not None:
                    value.append(val_2)
            except:
                pass
            
            try:
                variables = ", ".join(variables)
                value = ", ".join((list(map(str, value))))

                code = "def func({}):\n".format(variables)
                code += elif_st(keywords["statement"], keywords["var"])
                code += "    {}\n".format(st_code)
                code += "       return 1\n"
                code += "    else:\n"
                code += "       return 0\n\n"
                code += "{} = func({})".format(res_name[lang], value)
                return code
            except:
                return st_code
        return ref, constructor, 0, 0, 0, 0
     
    if question_class == PLAIN_ELSE:
        #reference function
        setattr(ref, res_name[lang], 1)

        #construction function
        def constructor(st_code):
            try:
                code = "def func():\n"
                code += "   if 0:\n"
                code += "       return 0\n"
                code += "   {}\n".format(" ".join(st_code.split()))
                code += "       return 1\n\n"
                code += "{} = func()".format(res_name[lang])
                return code
            except:
                return st_code
        return ref, constructor, 0, 0, 0, 0


if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check:
        ref, constructor = select_ref(
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            args.lang,
            data["params"]["raw_2"] if data["question_class"] == COMPOUND else None
        )

        msgs = {}
        
        constructor_func = constructor(data["answer"])
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
        if done_temp or total_temp != None:
            done = done_temp
            total = total_temp
        raw, formatdict = generate_params(qc, args.lang)

        if data["question_class"] == COMPOUND:
            out = {
                "question_class": data["question_class"],
                "correct": correct,
                "completed": completed,
                "progress": "{} / {}".format(done, total),
                "next": {
                    "question_class": qc,
                    "raw": raw,
                    "formatdict": formatdict
                }
            }
        else:
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
        if qc == 6:
            raw, formatdict = generate_params(qc, args.lang)
            out = {
                "question_class": qc,
                "progress": "{} / {}".format(done, total),
                "raw": raw,
                "formatdict": formatdict
            }
        else:
            raw, formatdict = generate_params(qc, args.lang)
            out = {
                "question_class": qc,
                "formatdict": formatdict,
                "progress": "{} / {}".format(done, total),
                "raw": raw,
            }

    core.json_output.wrap_to(out, "log")