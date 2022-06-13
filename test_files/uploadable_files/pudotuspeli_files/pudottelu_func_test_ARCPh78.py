import random
import test_core as core
from operator import itemgetter

GROUND_LEVEL = 0
DOWNFORCE = 1.5

st_func = {
    "fi": "pudota",
    "en": "drop"
}

_running_id = 0

fall_msgs = core.TranslationDict()
fall_msgs.set_msg("PrintTestVector", "fi", "Funktiokutsu:\n{call}\nKuva alkutilanteesta:\n{args}")
fall_msgs.set_msg("PrintTestVector", "en", "Function call:\n{call}\nInitial state:\n{args}")
fall_msgs.set_msg("PrintStudentResult", "fi", "Laatikoiden tila kutsun jälkeen (punaiset laatikot ovat putoamassa):\n{res}")
fall_msgs.set_msg("PrintStudentResult", "en", "State after call (red boxes are falling):\n{res}")
fall_msgs.set_msg("PrintReference", "fi", "Odotettu laatikoiden tila kutsun jälkeen (punaiset laatikot ovat putoamassa):\n{ref}")
fall_msgs.set_msg("PrintReference", "en", "Expected state (red boxes are falling):\n{ref}")

def _make_box(x, y, size):
    global _running_id
    _running_id += 1    
    return {
        "_id": _running_id,
        "x": x,
        "y": y,
        "w": size,
        "h": size,
        "vy": 0
    }

def gen_vector():
    v = []
    case_1 = []
    size = random.randint(20, 40)
    base_box_x = random.randint(100, 500)
    case_1.append(_make_box(base_box_x, 0, size))
    case_1.append(_make_box(base_box_x - size + 1, size, size))
    case_1.append(_make_box(base_box_x + size - 1, size, size))
    case_1.append(_make_box(base_box_x - size * 2 + 1, size * 2, size))
    case_1.append(_make_box(base_box_x + size * 2 - 1, size * 2, size))
    v.append([case_1])
    for _ in range(4):
        case = []
        for _ in range(random.randint(10, 20)):
            case.append(_make_box(
                random.randint(100, 500),
                random.randint(0, 250),
                40,
            ))
        v.append([case])
    
    return v
    
def ref_drop_func(objects):
    objects.sort(key=itemgetter("y"))
    for i, target in enumerate(objects):
        static = False
        if target["y"] <= GROUND_LEVEL:
            static = True
            target["vy"] = 0
            target["y"] = GROUND_LEVEL
            continue
            
        for other_target in objects[:i]:
            if target["y"] - target["h"] <= other_target["y"]:
                if abs(target["x"] - other_target["x"]) < min(target["w"], other_target["w"]):
                    static = True
                    target["vy"] = 0
                    target["y"] = other_target["y"] + target["h"]
                    break
        
        if not static:
            target["vy"] -= DOWNFORCE
            target["y"] += target["vy"]
            
    return objects

def objects_extractor(args, res, parsed):
    return args[0]
    
def objects_cloner(args):
    return [[box.copy() for box in args[0]]]
    
def fall_flag_validator(ref, res, parsed):
    falling_in_ref = [box["_id"] for box in ref if box["vy"] != 0]
    falling_in_res = [box["_id"] for box in res if box["vy"] != 0]
    assert falling_in_ref == falling_in_res

def initial_state_presenter(value):
    svg = ""
    max_y = 0
    for box in value[0]:
        max_y = max(box["y"], max_y)
    
    for box in value[0]:    
        svg += "<rect width='{w}' height='{h}' x='{x}' y='{rev_y}' stroke='black' fill='grey'/>\n".format(**box, rev_y=2 * max_y - box["y"]  - box["h"])
    bg = "<rect width='100%' height='100%' fill='white' />\n"
    return "{{{{{{svg|width={w}|height={h:.0f}\n{svg}}}}}}}".format(w=600, h=max_y * 2, svg=bg + svg)
    
def shortened_call_presenter(fname, args):
    args[0][0].pop("_id")
    call = fname + "([" + str(args[0][0]) + ", ...])"
    return call
    
def fall_presenter(value):
    svg = ""
    max_y = 0
    for box in value:
        max_y = max(box["y"], max_y)
        
    for box in value:
        if box["vy"] != 0:
            fill = "red"
        else:
            fill = "grey"
        svg += "<rect width='{w}' height='{h}' x='{x}' y='{y}' stroke='black' fill='{fill}'/>\n".format(**box, fill=fill, rev_y=2 * max_y - box["y"] - box["h"])
    bg = "<rect width='100%' height='100%' fill='white' />\n"
    return "{{{{{{svg|width={w}|height={h:.0f}\n{svg}}}}}}}".format(w=600, h=max_y * 2, svg=bg + svg)
    
    
fall_presenters = {
    "arg": initial_state_presenter,
    "call": shortened_call_presenter,
    "ref": fall_presenter,
    "res": fall_presenter
}
    
if __name__ == "__main__":
    files, lang = core.parse_command()
    st_mname = files[0]   
    st_module = core.load_module(st_mname, lang)
    if st_module:
        core.test_function(
            st_module, st_func, gen_vector, ref_drop_func, lang,
            custom_msgs=fall_msgs,
            argument_cloner=objects_cloner,
            result_object_extractor=objects_extractor,
            presenter=fall_presenters,
            validator=fall_flag_validator
        )
        core.test_function(
            st_module, st_func, gen_vector, ref_drop_func, lang,
            custom_msgs=fall_msgs,
            argument_cloner=objects_cloner,
            result_object_extractor=objects_extractor,
            presenter=fall_presenters,
            validator=fall_flag_validator,
            repeat=100
        )
            
        


    
