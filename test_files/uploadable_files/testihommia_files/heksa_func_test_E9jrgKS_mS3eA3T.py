import random
import sys
import test_core as core

st_function = {
    "en": "format_hex", 
    "fi": "muotoile_heksaluvuksi"
}

custom_msgs = core.TranslationDict()
custom_msgs.set_msg("PrintStudentResult", "fi", "Funktiosi tulos:\n{{{{{{svg|width=400|height=200\n<rect width='50' height='50' fill='red' />\n}}}}}}")

custom_msgs.set_msg("fail_return_none", "fi", dict(
    content="Funktio palautti Nonen.",
    triggers=["heksa-palautus"],
    hints=["Varmista että funktio '''palauttaa''' heksalukua esittävän merkkijonon."]
))
custom_msgs.set_msg("fail_return_none", "en", dict(
    content="Your function returned None.",
    triggers=["heksa-palautus"],
    hints=["Make sure the function '''returns''' the hexadecimal number string."]
))
custom_msgs.set_msg("info_print", "fi", dict(
    content="Funktio sisälsi tulostuksen.",
    triggers=["heksa-tulostus"],
    hints=["Tulosta funktion lopputulos '''pääohjelmassa''', älä funktion sisällä."]
))
custom_msgs.set_msg("info_print", "en", dict(
    content="The function printed something.",
    triggers=["heksa-tulostus"],
    hints=["Print the function's result in the '''main program''', not inside the function."]
))

def gen_vector():
    v = []
    for i in range(10):
        bits = 2 ** random.randint(3, 6)
        value = random.randint(1, 2 ** (bits // random.randint(1, 4)))
        v.append((value, bits))
    return v

def ref_func(v, bits):
    return hex(v).replace("0x", "").rjust(bits // 4, "0")

def validate_hex(ref, res, parsed):
    assert res is not None, "fail_return_none"
    assert ref == res
    
def info_print(res, parsed, output, ref, args, inps):
    if not output:
        raise core.NoAdditionalInfo
    
if __name__ == "__main__":
    files, lang = core.parse_command()
    st_mname = files[0]   
    st_module = core.load_module(st_mname, lang, inputs=["0", "8"])
    if st_module:
       core.test_function(
           st_module, st_function, gen_vector, ref_func, lang,
           custom_msgs=custom_msgs,
           validator=validate_hex,
           info_funcs=[info_print]
        )
       core.pylint_test(st_module, lang)
            
