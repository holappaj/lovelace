import json
import random
import test_core as core

# DEC: 0, 3
# BIN: 1, 4
# HEX: 2, 5

BIN_TO_DEC = 0
DEC_TO_BIN = 1
DEC_TO_HEX = 2
HEX_TO_DEC = 3
HEX_TO_BIN = 4
BIN_TO_HEX = 5

prefix = ["", "0b", "0x", "", "0b", "0x"]

res_name = {
    "fi": "tuloste",
    "en": "print"
}

def determine_question(history, completed, active):
    '''
    Determines what and if a question needs to be asked. 
    - Depends on cmd line argument and the amount of correct questions answered.
    '''
    required_repeats = 1

    if completed:
        return random.choice(active), None, None

    choices = []
    remaining = 0
    done = 0
    for cq in active:
        correct = history.count([cq, True])
        incorrect = history.count([cq, False])
        done += correct
        if correct < required_repeats or correct <= incorrect:
            choices.append(cq)
            remaining += max(required_repeats - correct, incorrect - correct)

    #if choices == []:
        #return random.choice(active), None, None

    return random.choice(choices), done, done + remaining

def generate_params(question_class, lang):
    '''
    - Generates all the parameters that are used in the questions. 
    - Returns them as a dictionary.
    - When parameters come in a list it also creates a formated dictionary
      where list is changed into a string.
    '''
    number = random.randint(257, 1e4)
    # BIN_TO_DEC, DEC_TO_BIN, HEX_TO_DEC, DEC_TO_HEX, HEX_TO_BIN, BIN_TO_HEX
    if question_class == BIN_TO_DEC:
        raw = {
            "num": bin(number)[2:]
        }
        return raw, raw

    if question_class == DEC_TO_BIN:
        raw = {
            "num": number
        }
        return raw, raw

    if question_class == HEX_TO_DEC:
        raw = {
            "num": hex(number)[2:]
        }
        return raw, raw

    if question_class == DEC_TO_HEX:
        raw = {
            "num": number
        }
        return raw, raw

    if question_class == HEX_TO_BIN:
        raw = {
            "num": hex(number)[2:]
        }
        return raw, raw

    if question_class == BIN_TO_HEX:
        raw = {
            "num": bin(number)[2:]
        }
        return raw, raw

def custom_msgs(question_class, st_code, keywords, constructor, var):
    '''
    - Messages that are shown to the person answering the questions. 
    - Message shown depends if you answer correctly or incorrectly.
    '''
    # Test the messages. They will be changed after I know what they do
    custom_msgs = core.TranslationDict()
    custom_msgs.set_msg("PrintStudentResult", "fi", "")
    custom_msgs.set_msg("SnippetTest", "fi", "")
    custom_msgs.set_msg("CorrectResult", "fi", "")
    custom_msgs.set_msg("IncorrectResult", "fi", "")
    custom_msgs.set_msg("fail_variable_value", "fi", "")
    #custom_msgs.set_msg("PrintStudentResult", "fi", "Lista, jota vastauksesi käytti ja vastauksesi:\n{}\n\nOdotetut muuttujien arvot:\n{} = {}".format(constructor, keywords["num"], var))
    custom_msgs.set_msg("GenericErrorMsg", "fi", "Syötettä tarkistettaessa tapahtui virhe.\nVarmista syötteen oikeinkirjoitus.")
    custom_msgs.set_msg("PrintReference", "fi", "")

    #custom_msgs.set_msg("PrintStudentResult", "en", "List used with your answer and your answer:\n{}\n\nExpected variable and value:\n{} = {}".format(constructor, keywords["num"], var))
    custom_msgs.set_msg("PrintStudentResult", "en", "")
    custom_msgs.set_msg("SnippetTest", "en", "")
    custom_msgs.set_msg("CorrectResult", "en", "")
    custom_msgs.set_msg("IncorrectResult", "en", "")
    custom_msgs.set_msg("fail_variable_value", "en", "")
    custom_msgs.set_msg("GenericErrorMsg", "en", "An error occurred while interpreting your input.  Make sure you didn't make typos.")
    custom_msgs.set_msg("PrintReference", "en", "")
    return custom_msgs

def select_ref(question_class, st_code, keywords, lang):
    '''
    - Creates first reference functions and then a constructor functions in a nested function for
      the different questions.
    - Reference function is variable and value set into an object with setattr function.
    - Constructor function is saved in the variable 'code'.
    - Returns reference function, constructor function and different variables that are used in the
      'custom_msgs' function
    '''
    ref = core.SimpleRef()
    # assuming a function is used to contain student's input for security
    def constructor(st_ans):
        code = "def func():\n"
        code+= "    a = '" + st_ans + "'.strip().lower().lstrip('" + prefix[question_class] + "').lstrip('0')\n"
        code+= "    return a\n"
        code+= "a = func()"
        return code

    if question_class == BIN_TO_DEC:
        setattr(ref, "a", str(int(keywords["num"], 2)))
        return ref, constructor, 0

    if question_class == DEC_TO_BIN:
        setattr(ref, "a", bin(keywords["num"])[2:])
        return ref, constructor, 0

    if question_class == HEX_TO_DEC:
        setattr(ref, "a", str(int(keywords["num"], 16)))
        return ref, constructor, 0

    if question_class == DEC_TO_HEX:
        setattr(ref, "a", hex(keywords["num"])[2:])
        return ref, constructor, 0

    if question_class == HEX_TO_BIN:
        setattr(ref, "a", bin(int(keywords["num"], 16))[2:])
        return ref, constructor, 0

    if question_class == BIN_TO_HEX:
        setattr(ref, "a", hex(int(keywords["num"], 2))[2:])
        return ref, constructor, 0


if __name__ == "__main__":
    data, args = core.parse_command()
    if args.check:
        ref, constructor, var = select_ref( # ref == var
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            args.lang
        )
        constructor_func = constructor(data["answer"])
        msgs = custom_msgs(
            data["question_class"],
            data["answer"],
            data["params"]["raw"],
            constructor_func,
            var # == ref
        )
        correct = core.test_code_snippet(
            data["answer"],
            constructor,
            ref, # == var
            args.lang,
            msgs
        )
        try: # prevent error from "None/None"
            done, total = [int(x) for x in data["progress"].split("/")]
        except ValueError:
            done, total = 7, 6

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
            "correct": False,
            "raw": raw
        }
    core.json_output.wrap_to(out, "log")
