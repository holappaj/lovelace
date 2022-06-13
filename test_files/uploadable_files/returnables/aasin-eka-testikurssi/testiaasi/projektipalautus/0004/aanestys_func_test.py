import random
import test_core as core
from string import ascii_lowercase

st_prompt_function = {
    "fi": "aanesta",
    "en": "vote"
}

st_result_function = {
    "fi": "nayta_tulokset",
    "en": "show_results"
}

poll_keys = {
    "fi": ["jaa", "ei", "eos", "virhe"],
    "en": ["yea", "nay", "idk", "error"]
}

result_msgs = core.TranslationDict()
result_msgs.set_msg("PrintStudentResult", "fi", "Funktio tulosti seuraavanlaiset tulokset: {parsed}")
result_msgs.set_msg("PrintStudentResult", "en", "Your function printed the following results: {parsed}")
result_msgs.set_msg("PrintReference", "fi", "Oikeat tulokset: {ref}")
result_msgs.set_msg("PrintReference", "en", "Correct results: {ref}")

def gen_vector():
    v = []
    for i in range(5):
        poll = {}
        for key in poll_keys[lang]:
            poll[key] = random.randint(0, 10)
        v.append([poll])
    return v

def gen_input_vector():
    v = []
    for i in range(5):
        inps = []
        for j in range(10):
            key_number = random.randint(0, 3)
            if key_number == 3:
                inps.append("".join(random.choices(ascii_lowercase, k=3)))
            else:
                inps.append(poll_keys[lang][key_number])
        v.append(inps)
    return v
    
def ref_prompt_function(args, inputs):
    poll = args[0]
    for key in inputs:
        try:
            poll[key] += 1
        except KeyError:
            poll[poll_keys[lang][-1]] += 1
    
    return poll
    
def ref_result_function(poll):
    return poll
    
def poll_parser(output):
    result_dict = {}
    for line in output.split("\n"):
        if line.strip():
            result_dict[line.split(":")[0].strip().lower()] = line.count("#")
    return result_dict
    
def poll_cloner(args):
    return [args[0].copy()]
    
def poll_extractor(args, res, parsed):
    return args[0]
    
def one_line_input_presenter(value):
    out = "{{{\n"
    out += ", ".join(value)
    out += "\n}}}"
    return out

def results_presenter(value):
    out = "\n{{{\n"
    for key, value in value.items():
        out += "{}: {}\n".format(key, value)
    out += "}}}"
    return out
    
prompt_presenters = {
    "input": one_line_input_presenter,
    "res": results_presenter,
    "ref": results_presenter,
}

result_presenters = {
    "parsed": results_presenter,
    "ref": results_presenter,
}

if __name__ == "__main__":
    files, lang = core.parse_command()
    st_mname = files[0]   
    st_module = core.load_module(
        st_mname, lang,
        allow_output=True,
        inputs=["".join(random.choices(ascii_lowercase, k=3)) for i in range(10)]
    )
    if st_module:
        core.test_function(
            st_module, st_prompt_function, gen_vector, ref_prompt_function, lang,
            inputs=gen_input_vector,
            presenter=prompt_presenters,
            result_object_extractor=poll_extractor,
            argument_cloner=poll_cloner,
            repeat=10,
            ref_needs_inputs=True
        )
        core.test_function(
            st_module, st_result_function, gen_vector, ref_result_function, lang,
            custom_msgs=result_msgs,
            presenter=result_presenters,
            hide_output=False,
            test_recurrence=False,
            output_parser=poll_parser,
            validator=core.parsed_result_validator
        )

