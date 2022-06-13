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
LIST_GET_ITEM_2D = 9
LIST_ITEM_ASSIGN = 10
LIST_ITEM_ASSIGN_2D = 11
LIST_ITEM_MOVE = 12
LIST_ITEM_MOVE_IDX_VAR = 13
LIST_ITEM_MOVE_IDX_VAR_2D = 14 

res_name = {
    "fi": "tuloste",
    "en": "print"
}

same_id_name = {
    "fi": "sama_lista",
    "en": "same_list"
}
    
def highlight_wrap(code):
    code = "{{{highlight=python3\n" + code + "\n}}}"
    return code

def generate_matrix(w, h):
    matrix = []
    for r in range(h):
        matrix.append([])
        for c in range(w):
            matrix[-1].append(random.randint(1, 9))
    return matrix
    
def generate_setup(matrix, var, base_indent=0):
    setup = base_indent * " " + "{} = [\n".format(var)
    for row in matrix:
        setup += (base_indent + 4) * " " + repr(row) + ",\n"
    setup += base_indent * " " + "]\n"
    return setup    
    
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

    if question_class in (LIST_GET_ITEM_2D, LIST_ITEM_ASSIGN_2D):
        rows = random.randint(4, 8)
        cols = random.randint(4, 8)
        row_idx = random.randint(0, rows - 1)
        col_idx = random.randint(0, cols - 1)
        var = random.choice(INT_LIST_ITEM_NAMES[lang])
        list_var = random.choice(INT_LIST_NAMES[lang])
        matrix = generate_matrix(cols, rows)
        setup = generate_setup(matrix, list_var)
        formatdict = {
            "var": var,
            "list_var": list_var,
            "row_idx": row_idx,
            "col_idx": col_idx,
            "rows": rows,
            "cols": cols,
            "setup": highlight_wrap(setup)
        }
        raw = {
            "var": var,
            "list_var": list_var,
            "row_idx": row_idx,
            "col_idx": col_idx,
            "rows": rows,
            "cols": cols,
        }        
        return raw, formatdict
        
    if question_class == LIST_ITEM_ASSIGN:
        list_var = random.choice(INT_LIST_NAMES[lang])
        var = random.choice(INT_LIST_ITEM_NAMES[lang])
        i = random.randint(0, 10)
        raw = {
            "list_var": list_var,
            "var": var,
            "i": i
        }
        return raw, raw
        
    if question_class == LIST_ITEM_MOVE:
        list_var_1, list_var_2 = random.choice(LIST_COPY_NAMES[lang])
        i = random.randint(0, 10)
        raw = {
            "list_var_1": list_var_1,
            "list_var_2": list_var_2,
            "i": i
        }
        return raw, raw
            
    if question_class == LIST_ITEM_MOVE_IDX_VAR:
        list_var_1, list_var_2 = random.choice(LIST_COPY_NAMES[lang])
        idx_var = random.choice(INDEX_VAR_NAMES[lang])
        raw = {
            "list_var_1": list_var_1,
            "list_var_2": list_var_2,
            "idx_var": idx_var
        }
        return raw, raw
        
    if question_class == LIST_ITEM_MOVE_IDX_VAR_2D:
        list_var_1, list_var_2 = random.choice(LIST_COPY_NAMES[lang])        
        idx_var_1, idx_var_2 = random.choice(MATRIX_INDEX_NAMES[lang])
        rows = random.randint(4, 8)
        cols = random.randint(4, 8)
        matrix = generate_matrix(cols, rows)
        setup = generate_setup(matrix, list_var_1)
        matrix = generate_matrix(cols, rows)
        setup += generate_setup(matrix, list_var_2)
        raw = {
            "list_var_1": list_var_1,
            "list_var_2": list_var_2,
            "idx_var_1": idx_var_1,
            "idx_var_2": idx_var_2,
            "rows": rows,
            "cols": cols
        }
        formatdict = {
            "list_var_1": list_var_1,
            "list_var_2": list_var_2,
            "idx_var_1": idx_var_1,
            "idx_var_2": idx_var_2,
            "rows": rows,
            "cols": cols,
            "setup": highlight_wrap(setup)
        }
        return raw, formatdict

        
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
            code = "{} = {}\n".format(keywords["var"], var)
            code += "_id = id({})\n".format(keywords["var"])
            code += st_code + "\n"
            code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["var"])
                
            return code
                
        return ref, constructor, res

    if question_class == LIST_COPY:
        var = random.sample(range(1,100), 5)
        res = var[:]
        setattr(ref, keywords["var_1"], var)
        setattr(ref, keywords["var_2"], res)
        setattr(ref, same_id_name[lang], False)

        def constructor(st_code):
            try:
                code = "{} = {}\n".format(keywords["var_1"], var)
                code += "_id = id({})\n".format(keywords["var_1"])
                code += st_code + "\n"
                code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["var_2"])
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == LIST_SLICE:
        var = random.sample(range(1,100), 10)
        res = var[keywords["i0"]:keywords["i1"] + 1]
        
        setattr(ref, keywords["var_1"], var)
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
        setattr(ref, same_id_name[lang], True)

        def constructor(st_code):
            try:
                code = "{} = {}\n".format(keywords["var"], var)
                code += "_id = id({})\n".format(keywords["var"])
                code += st_code + "\n"
                code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["var"])
                return code
            except:
                return st_code
        return ref, constructor, res

    if question_class == LIST_PRINT_ITEM:
        var = random.sample(range(1,100), 11)
        res = var[keywords["i"]]
        
        ref = lambda x: str(res)

        def constructor(st_code):
            try:
                code = "{} = {}\n".format(keywords["var"], var)
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

    if question_class == LIST_GET_ITEM_2D:
        matrix = generate_matrix(keywords["cols"], keywords["rows"])
        setattr(ref, keywords["var"], matrix[keywords["row_idx"]][keywords["col_idx"]])
        
        def constructor(st_code):
            code = generate_setup(matrix, keywords["list_var"])
            code += st_code
            return code
            
        return ref, constructor, 0

    if question_class == LIST_ITEM_ASSIGN:
        vector = random.sample(range(1,100), 11)
        assign = random.randint(101, 200)
        copy = vector[:]
        copy[keywords["i"]] = assign
        setattr(ref, keywords["list_var"], copy)
        setattr(ref, same_id_name[lang], True)
        
        def constructor(st_code):            
            code = "{} = {}\n".format(keywords["list_var"], repr(vector))
            code += "{} = {}\n".format(keywords["var"], repr(assign))
            code += "_id = id({})\n".format(keywords["list_var"])
            code += st_code + "\n"
            code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["list_var"])
            return code
        
        return ref, constructor, 0  

    if question_class == LIST_ITEM_ASSIGN_2D:
        matrix = generate_matrix(keywords["cols"], keywords["rows"])
        assign = random.randint(10, 20)
        copy = []
        for row in matrix:
            copy.append(row[:])
        copy[keywords["row_idx"]][keywords["col_idx"]] = assign
        setattr(ref, keywords["list_var"], copy)
        setattr(ref, same_id_name[lang], True)
        
        def constructor(st_code):            
            code = generate_setup(matrix, keywords["list_var"])
            code += "{} = {}\n".format(keywords["var"], repr(assign))
            code += "_id = id({})\n".format(keywords["list_var"])
            code += st_code + "\n"
            code += "{} = id({}) == _id\n".format(same_id_name[lang], keywords["list_var"])
            return code
        
        return ref, constructor, 0  
        
    if question_class == LIST_ITEM_MOVE:
        vector_1 = random.sample(range(1,100), 11)
        vector_2 = [0] * 11
        result = [0] * 11
        result[keywords["i"]] = vector_1[keywords["i"]]
        setattr(ref, keywords["list_var_2"], result)
        
        def constructor(st_code):
            code = "{} = {}\n".format(keywords["list_var_1"], repr(vector_1))
            code += "{} = {}\n".format(keywords["list_var_2"], repr(vector_2))
            code += st_code + "\n"
            return code
            
        return ref, constructor, 0
        
    if question_class == LIST_ITEM_MOVE_IDX_VAR:
        vector_1 = random.sample(range(1,100), 11)
        vector_2 = [0] * 11
        result = [0] * 11
        i = random.randint(0, 10)
        result[i] = vector_1[i]
        setattr(ref, keywords["list_var_2"], result)
        
        def constructor(st_code):
            code = "{} = {}\n".format(keywords["list_var_1"], repr(vector_1))
            code += "{} = {}\n".format(keywords["list_var_2"], repr(vector_2))
            code += "{} = {}\n".format(keywords["idx_var"], repr(i))
            code += st_code + "\n"
            return code
            
        return ref, constructor, 0

    if question_class == LIST_ITEM_MOVE_IDX_VAR_2D:
        matrix_1 = generate_matrix(keywords["cols"], keywords["rows"])
        matrix_2 = generate_matrix(keywords["cols"], keywords["rows"])
        col_idx = random.randint(0, keywords["cols"] - 1)
        row_idx = random.randint(0, keywords["rows"] - 1)
        copy = []
        for row in matrix_2:
            copy.append(row[:])
        copy[row_idx][col_idx] = matrix_1[row_idx][col_idx]
        setattr(ref, keywords["list_var_2"], copy)
        
        def constructor(st_code):
            code = generate_setup(matrix_1, keywords["list_var_1"])
            code += generate_setup(matrix_2, keywords["list_var_2"])
            code += "{} = {}\n".format(keywords["idx_var_1"], repr(col_idx))
            code += "{} = {}\n".format(keywords["idx_var_2"], repr(row_idx))
            code += st_code + "\n"
            return code
            
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

        if data["question_class"] == LIST_PRINT_ITEM:
            presenters = {
                "ref_vars": lambda x: x
            }
            msgs = core.TranslationDict()
            msgs.set_msg("PrintStudentResult", "fi", "")
            msgs.set_msg("PrintStudentResult", "en", "")
            msgs.set_msg("PrintStudentOutput", "fi", "Koodin tuloste:\n{{{{{{\n{output}\n}}}}}}")
            msgs.set_msg("PrintStudentOutput", "en", "Code output:\n{{{{{{\n{output}\n}}}}}}")
            msgs.set_msg("PrintReference", "fi", "Mallituloste:\n{{{{{{\n{ref}\n}}}}}}")
            msgs.set_msg("PrintReference", "en", "Reference output:\n{{{{{{\n{ref}\n}}}}}}")
                        
            correct = core.test_code_snippet(
                data["answer"],
                constructor,
                ref,
                args.lang,
                custom_msgs=msgs,
                validator=core.parsed_result_validator,
                presenter=presenters,
                hide_output=False
            )
        else:
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
        qc, done_temp, total_temp = core.determine_question(
            data["history"], completed,
            args.questions, args.target
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
        qc, done, total = core.determine_question(
            data["history"], data["completed"],
            args.questions, args.target
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