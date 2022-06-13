import json
import random
import test_core as core

phases = 5

def choose_phase(history):
    done = [x[1] for x in history].count(True)
    return done

def get_question(phase):
    if phase == 0:
        raw = {
            "var": "x",
            "value": 4
        }
        return 0, raw
    elif phase == 1:
        raw = {
            "var": "y",
            "value": 2
        }
        return 0, raw
    elif phase == 2:
        raw = {
            "var_1": "x",
            "var_2": "y",
            "res_var": "k"
        }
        return 1, raw
    elif phase == 3:
        raw = {
            "var": "k",
            "value": 7,
            "res_var": "y1"
        }
        return 2, raw
    elif phase == 4:
        raw = {
            "var": "k",
            "value": 159,
            "res_var": "y2"
        }
        return 2, raw

def dummy_constructor(st_code):
    return st_code
        
def select_ref(phase, keywords, lang):
    ref = core.SimpleRef()
    if phase in (0, 1):
        setattr(ref, keywords["var"], keywords["value"])
        return ref, dummy_constructor
    elif phase == 2:
        x_val = random.randint(1, 100)
        y_val = random.randint(1, 100)
        setattr(ref, keywords["var_1"], x_val)
        setattr(ref, keywords["var_2"], y_val)
        setattr(ref, keywords["res_var"], y_val / x_val)
        
        def constructor(st_code):
            code = ""
            code += "{} = {}\n".format(keywords["var_1"], x_val)
            code += "{} = {}\n".format(keywords["var_2"], y_val)
            code += st_code
            return code
        
        return ref, constructor
    else:
        k_val = round(random.random() * 2, 1)
        setattr(ref, keywords["var"], k_val)
        setattr(ref, keywords["res_var"], k_val * keywords["value"])
    
        def constructor(st_code):
             code = ""
             code += "{} = {}\n".format(keywords["var"], k_val)
             code += st_code
             return code
             
        return ref, constructor
        


        
if __name__ == "__main__":

    data, args = core.parse_command()
    phase = choose_phase(data["history"])
    if args.check:
        ref, constructor = select_ref(
            phase % phases,
            data["params"]["raw"],
            args.lang
        )
        correct = core.test_code_snippet(data["answer"], constructor, ref, args.lang)
        st_module = core.load_module("temp_module.py")
        core.pylint_test(
            st_module, args.lang,
            info_only=False,
            validator=core.strict_pylint_validator,
            extra_options=["--disable=missing-final-newline,missing-module-docstring,invalid-name"]
        )
        
        if correct:
            phase += 1
        
        if phase == phases:
            completed = True
        else:
            completed = False
        qc, raw = get_question(phase % phases)
        out = {
            "question_class": data["question_class"],
            "correct": correct,
            "completed": completed,
            "progress": "{} / {}".format(phase, phases),
            "next": {
                "question_class": qc,
                "formatdict": raw,
                "raw": raw
            }
        }
    else:
        phase = choose_phase(data["history"])
        done, total = phase, phases
            
        qc, raw = get_question(phase % phases)
        out = {
                "question_class": qc,
                "formatdict": raw,
                "progress": "{} / {}".format(done, total),
                "raw": raw,
            }
            
    core.json_output.wrap_to(out, "log")
            
        