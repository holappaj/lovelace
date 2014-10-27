# -*- coding: utf-8 -*-
"""Parser for inline wiki markup tags that appear in paragraphs, tables etc."""

import re
# TODO: Add more syntax highlighters!
# TODO: {{{#!python {}}}} breaks up!
# TODO: |forcedownload or |forceview for links
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from courses.highlighters import highlighters

class Tag:
    """One markup tag type."""

    def __init__(self, tagname, tagbegin, tagend, tagre):
        self.name = tagname
        self.begin = tagbegin
        self.end = tagend
        self.re = tagre
        self.options = None

    def set_options(self, options):
        self.options = options

    def htmlbegin(self, options=None):
        """Returns the HTML equivalent begin tag of the inline wiki markup."""
        if not self.options and not options:
            return "<%s>" % (self.name)
        elif self.options and not options:
            return "<%s %s>" % (self.name, " ".join("%s=\"%s\"" % kv for kv in self.options.items()))
        elif not self.options and options:
            return "<%s %s>" % (self.name, " ".join("%s=\"%s\"" % kv for kv in options.items()))
        else:
            return "<%s %s>" % (self.name, " ".join("%s=\"%s\"" % kv for kv in dict(self.options.items() + options.items()).items()))
    
    def htmlend(self):
        """Returns the HTML equivalent end tag."""
        return "</%s>" % (self.name)

    def lb(self):
        """Length of the beginning wiki markup tag."""
        return len(self.begin)
    def le(self):
        """Length of the ending wiki markup tag."""
        return len(self.end)

# A library of different tags supported by the wiki markup
tags = {"bold":   Tag("strong", "'''", "'''", re.compile(r"[']{3}(?P<bold_italic>[']{2})?.+?(?P=bold_italic)?[']{3}")),
        "italic": Tag("em", "''", "''", re.compile(r"[']{2}.+?[']{2}")),
        "pre":    Tag("code", "{{{", "}}}", re.compile(r"[{]{3}(?P<highlight>\#\!(%s) )?.+?[}]{3}" % ("|".join(highlighters.keys())))),
        "dfn":    Tag("dfn", "", "", re.compile(r"")),
        "mark":   Tag("mark", "!!!", "!!!", re.compile(r"[\!]{3}.+?[\!]{3}")),
        "anchor": Tag("a", "[[", "]]", re.compile(r"\[\[(?P<address>.+?)([|](?P<link_text>.+?))?\]\]")),} 

def parsetag(tagname, unparsed_string):
    """Parses one tag and applies it's settings. Generates the HTML."""
    tag = tags[tagname]
    hilite = address = link_text = None
    parsed_string = ""
    cursor = 0
    for m in re.finditer(tag.re, unparsed_string):
        parsed_string += unparsed_string[cursor:m.start()]
        
        try:
            hilite = m.group("highlight") # Special for code
        except IndexError:
            pass
        try:
            address = m.group("address") # Special for anchor
            link_text = m.group("link_text") # Special for anchor
        except IndexError:
            pass
        if hilite:
            code_string = m.group(0)[tag.lb()+len(hilite):-tag.le()]
            for escaped, unescaped in {"&lt;":"<", "&gt;":">", "&amp;":"&"}.items():
                code_string = code_string.replace(escaped, unescaped)
            hilite = hilite.strip("#! ")
            parsed_string += tag.htmlbegin({"class":"highlight-"+hilite.strip("#! ")})
            parsed_string += highlight(code_string, highlighters[hilite](), HtmlFormatter(nowrap=True)).rstrip("\n")
            parsed_string += tag.htmlend()
        elif address:
            contents = link_text or address
            parsed_string += tag.htmlbegin({"href":address})
            parsed_string += contents
            parsed_string += tag.htmlend()
            #print tag.htmlbegin({"href":address}) + contents + tag.htmlend()
        else:
            contents = m.group(0)[tag.lb():-tag.le()]
            parsed_string += tag.htmlbegin()
            parsed_string += contents
            parsed_string += tag.htmlend()

        cursor = m.end()
        hilite = False
    parsed_string += unparsed_string[cursor:]

    return parsed_string

def parseblock(blockstring):
    """A multi-pass parser for inline markup language inside paragraphs."""
    # TODO: Start with pre tags to prevent formatting inside pre
    #       - Perhaps use a state machine to determine, whether inside pre
    #if len(re.findall("'''", blockstring)) % 2:
        # TODO: Raise an exception instead, show the exception at the end of the block in red
        #return blockstring

    parsed_string = parsetag("pre", blockstring)
    parsed_string = parsetag("bold", parsed_string)
    parsed_string = parsetag("italic", parsed_string)
    parsed_string = parsetag("mark", parsed_string)
    parsed_string = parsetag("anchor", parsed_string)

    return parsed_string

# Some test code
if __name__ == "__main__":
    block1 = "'''alku on boldia ''ja valissa on italistoitua'' ja sitten jatkuu boldi'''"
    block2 = "alku ei ole boldia '''''mutta sitte tulee itaboldi kohta'' joka jatkuu boldina''' ja loppuu epaboldina"
    block3 = "normi '''bold''' normi '''bold''' normi ''italic'' normi '''bold''' normi ''italic'' '''bold''' normi"
    block4 = "one '''doesn't''' simply walk into mordor"
    block5 = "jeejee ''ita'''itabold'''''"

    blocks = [block1, block2, block3, block4, block5]

    for i, block in enumerate(blocks):
        print("Test %02d:" % i)
        parseblock(block)
        print()
