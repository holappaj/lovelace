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

compound_templates = {
    "fi": [
        [
            "onko {{{{{{{var}}}}}}}-muuttujan arvo {operation} kuin {{{{{{#!python3 {val}}}}}}}",
        ],
        [
            "onko {{{{{{{var}}}}}}}-muuttujan arvo {boolean_name} (ei vertailuoperaattoreita!)",
        ],
        [
            "onko {{{{{{{var}}}}}}}-muuttujan pituus {operation} kuin {{{{{{#!python3 {val}}}}}}}",
        ],
        [
            "onko {{{{{{{var}.{mname}}}}}}}-kutsun paluuarvo {template_args} {boolean_name} (ei vertailuoperaattoreita)",
        ],
        [
            "onko {{{{{{{var}.{mname}}}}}}}-kutsun paluuarvo {template_args} sama kuin {{{{{{#!python3 {val}}}}}}}",
        ],
        [
            "onko {{{{{{{var}}}}}}} {operation} kuin {{{{{{{var_2}}}}}}}"
        ]
    ],
    "en": [
        [
            "is the value of {{{{{{{var}}}}}}} {operation} {{{{{{#!python3 {val}}}}}}}",
        ],
        [
            "is the value of {{{{{{{var}}}}}}} {boolean_name} (no comparison operators)",
        ],
        [
            "it the length of {{{{{{{var}}}}}}} {operation} {{{{{{#!python3 {val}}}}}}}"
        ],
        [
            "is the return value of {{{{{{{var}.{mname}}}}}}} call {boolean_name} {template_args} (no comparison operators).",
        ],
        [
            "is the return value of {{{{{{{var}.{mname}}}}}}} call equal to {{{{{{#!python3 {val}}}}}}} {template_args}.",
        ],
        [
            "is {{{{{{{var}}}}}}} {operation} {{{{{{{var_2}}}}}}}"
        ]
    ]
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
    elif qc == LEN_COMPARISON:
        return gen_var_len(operation, val)
    elif qc == METHOD_RETURN_VALUE:
        return gen_string(
            mname,
            args,
            boolean
        )
    elif qc == METHOD_RETURN_VALUE_EQUALS:
        return gen_var_val(
            val,
            mname = mname,
            args = args,
        )
    elif qc == VARIABLE_COMPARISON:
        val = random.randint(1, 100)
        vars = gen_var_val(val, op=operation)
        return [((v[0], val), v[1]) for v in vars]

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
    body = random_string(random.randint(3, 8))
    match = "".join(args)
    nomatch = str(random.randint(1, 999))

    if boolean == True:
        if mname == "startswith":
            return [
                (match + body + nomatch, 1),
                (nomatch + body, 0),
                (nomatch + match + body + nomatch, 0)
            ]
        elif mname == "endswith":
            return [
                (nomatch + body + match, 1),
                (body + nomatch, 0),
                (nomatch + match + body + nomatch, 0)
            ]
    else:
        if mname == "startswith":
            return [
                (match + body + nomatch, 0),
                (nomatch + body, 1),
                (nomatch + match + body + nomatch, 1)
            ]
        elif mname == "endswith":
            return [
                (nomatch + body + match, 0),
                (body + nomatch, 1),
                (nomatch + match + body + nomatch, 1)
            ]

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
            base = [random.choice("0123456789") for i in range(10)]
            match = base[:]
            match.extend(args * val)
            random.shuffle(match)
            match = "".join(match)
            nomatch = base[:]
            nomatch.extend(args * val * 2)
            nomatch = "".join(nomatch)
            return [(match, 1), (nomatch, 0)]
        if mname == "replace":
            if len(args) == 2:
                match = args[0] * len(val)
                nomatch = [random.choice("0123456789") for i in range(10)]
                nomatch.extend(list(match))
                random.shuffle(nomatch)
                nomatch = "".join(nomatch)
            else:
                match = args[0] * len(val)
                nomatch = args[0] * (len(val) + random.randint(1, 4))
            return [(match, 1), (nomatch, 0)]
        if mname == "lower":
            return [(val.upper(), 1), (val.lower(), 1), (str(random.randint(0, 9)), 0)]
        if mname == "rstrip":
            return [
                (val + "\t" + " " * random.randint(1, 5), 1),
                (" " * random.randint(1, 5) + val + "\t" + " " * random.randint(1, 5), 0),
                (" " * random.randint(1, 5) + val, 0),
                (val, 1),
            ]
        if mname == "strip":
            start = val[:5]
            end = val[5:]
            nomatch = start + " " + end
            return [
                (val + " " * random.randint(1, 5), 1),
                (" " * random.randint(1, 5) + val + "\t" + " " * random.randint(1, 5), 1),
                (" " * random.randint(1, 5) + val, 1),
                (nomatch, 0),
                (val, 1),
            ]
        if mname == "upper":
            return [(val.lower(), 1), (val.upper(), 1), (str(random.randint(0, 9)), 0)]

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
        val = random.randint(2, 10)
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
            template_args = yes_arguments[lang] + "{{{#!python3 " + ", ".join(repr(a) for a in args) + "}}}"
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
        args = method.gen_args(lang)
        val = method.gen_comp(lang)
        if args != []:
            template_args = yes_arguments[lang] + "{{{#!python3 " + ", ".join(repr(a) for a in args) + "}}}"
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
        formatdict = {
            "statement": statement,
            "var": var,
            "operation": operation[1][lang],
            "var_2": var_2
        }
        return raw, formatdict

    if question_class == COMPOUND:
        conn = random.choice(connectors)
        full_raw = {}
        full_kw = {
            "conn": conn,
            "statement": statement
        }
        
        for i in range(1, 3):
            qcs = questions_available[:]
            try:
                cts.remove(6)
                cts.remove(7)
            except:
                pass
            qc = random.choice(qcs)
            qc_tmpl = compound_templates[lang][ct_id][0]
            raw, kw = generate_params(qc, land)
            question = qc_tmpl.format(**kw)
            full_kw["template_" + str(i)] = question
            full_raw["raw_" + str(i)] = raw

        return full_raw, full_kw

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
        var_names = [keywords["var"]]
    elif question_class == VARIABLE_VALUE:
        test_vars = gen_var(
            question_class,
            boolean=keywords["boolean"]
        )
        var_names = [keywords["var"]]
    elif question_class == LEN_COMPARISON:
        test_vars = gen_var(
            question_class,
            val=keywords["val"],
            operation=keywords["operation"][0]
        )
        var_names = [keywords["var"]]
    elif question_class == METHOD_RETURN_VALUE:
        test_vars = gen_var(
            question_class,
            mname=keywords["mname"],
            args=keywords["args"],
            boolean=keywords["boolean"]
        )
        var_names = [keywords["var"]]
    elif question_class == METHOD_RETURN_VALUE_EQUALS:
        test_vars = gen_var(
            question_class,
            val=keywords["val"],
            mname=keywords["mname"],
            args=keywords["args"],
        )
        var_names = [keywords["var"]]
    elif question_class == VARIABLE_COMPARISON:
        test_vars = gen_var(
            question_class,
            operation=keywords["operation"][0],
            var_2=keywords["var_2"]
        )
        var_names = [keywords["var"], keywords["var_2"]]    
    elif question_class == COMPOUND:
        keywords_1 = keywords["raw_1"]
        keywords_2 = keywords["raw_2"]
        test_vars_1 = gen_var(
            keywords["qc"],
            val=keywords.get("val", ""),
            operation=keywords.get("operation", [""])[0],
            args=keywords.get("args", ""),
            mname=keywords.get("mname", ""),
            var_2=keywords.get("var_2", ""),
            boolean=keywords.get("boolean", "")
        )
        test_vars_2 = gen_var(
            keywords_2["qc"],
            val=keywords_2.get("val", ""),
            operation=keywords_2.get("operation", [""])[0],
            args=keywords_2.get("args", ""),
            mname=keywords_2.get("mname", ""),
            var_2=keywords_2.get("var_2", ""),
            boolean=keywords_2.get("boolean", "")
        )
        test_vars_1 = test_vars_1 * len(test_vars_2)
        test_vars_2 = test_vars_2 * len(test_vars_1)
        random.shuffle(test_vars_2)
        compiled = []
        for (var_1, expected_1), (var_2, expected_2) in zip(test_vars_1, test_vars_2):
            case = []
            if isinstance(var_1, tuple):
                case.extend(var_1)
            else:
                case.append(var_1)
            if instance(var_2, tuple):
                case.extend(var_2)
            else:
                case.append(var_2)
            expected = eval("{} {} {}".format(expected_1, keywords["conn"], expected_2))
            compiled.append((tuple(case), expected))
        var_names = []
        var_names.append(keywords["var"])
        if "var_2" in keywords:
            var_names.append(keywords["var_2"])
        var_names.append(keywords_2["var"])
        if "var_2" in keywords_2:
            var_names.append(keywords_2["var_2"])
        test_vars = compiled
    
    ref = core.SimpleRef()
    for i, (_, expected) in enumerate(test_vars, start=1): 
        setattr(ref, "{}_{}".format(res_name[lang], i), expected)
        
    def constructor(st_code):
        try: 
            code = "def func({}):\n".format(", ".join(var_names))
            code += statement_constructor(st_code, keywords["statement"])
            for i, (var, _) in enumerate(test_vars, start=1): 
                if isinstance(var, tuple):
                    code += "{} = func({})\n".format(
                        "{}_{}".format(res_name[lang], i),
                        ", ".join(repr(v) for v in var) 
                    )
                else:
                    code += "{} = func({})\n".format("{}_{}".format(res_name[lang], i), repr(var))
            return code
        except:
            return st_code
    
    return ref, constructor


    

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
    questions_available = args.questions
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
        if data["completed"]:
            done, total = [int(x) for x in data["progress"].split("/")]
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