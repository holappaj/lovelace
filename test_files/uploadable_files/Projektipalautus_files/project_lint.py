import random
import test_core as core

class FakeModule(object):
    pass


msgs = core.TranslationDict()
msgs.set_msg("EOFError", "fi", "Sijoita kaikki syöttekyselyt {{{{{{#!python3 if __name__ == \"__main__\"}}}}}} lohkon alle.")
msgs.set_msg("EOFError", "en", "Place all input prompts under {{{{{{#!python3 if __name__ == \"__main__\"}}}}}}.")

if __name__ == "__main__":
    files, lang = core.parse_command()
    for mname in files:
        if mname.endswith(".py"):
            st_module = FakeModule()
            st_module.__file__ = mname
            core.pylint_test(st_module, lang, info_only=True, extra_options=["--disable=import-error"])
    
