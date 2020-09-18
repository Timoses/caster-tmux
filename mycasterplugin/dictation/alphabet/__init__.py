from dragonfly import Function, Choice, MappingRule, Text, Key

from mycastervoice import Plugin
from mycastervoice.util.dragonfly import CCRRule


def caster_alphabet():
    return {
        "arch"    : "a",
        "brov"    : "b",
        "char"    : "c",
        "delta"   : "d",
        "echo"    : "e",
        "foxy"    : "f",
        "goof"    : "g",
        "hotel"   : "h",
        "India"   : "i",
        "julia"   : "j",
        "kilo"    : "k",
        "Lima"    : "l",
        "Mike"    : "m",
        "Novakeen": "n",
        "oscar"   : "o",
        "prime"   : "p",
        "Quebec"  : "q",
        "Romeo"   : "r",
        "Sierra"  : "s",
        "tango"   : "t",
        "uniform" : "u",
        "victor"  : "v",
        "whiskey" : "w",
        "x-ray"   : "x",
        "yankee"  : "y",
        "Zulu"    : "z",
    }

def get_alphabet_choice(spec):
    return Choice(spec, caster_alphabet())

def letters(big, dict1, dict2, letter):
    '''used with alphabet.txt'''
    d1 = str(dict1)
    if d1 != "":
        Text(d1).execute()
    if big:
        Key("shift:down").execute()
    letter.execute()
    if big:
        Key("shift:up").execute()
    d2 = str(dict2)
    if d2 != "":
        Text(d2).execute()

def letters2(big, letter):
    if big:
        Key(letter.capitalize()).execute()
    else:
        Key(letter).execute()

class Alphabet(MappingRule):
    mapping = {
        "[<big>] <letter>":
            Function(letters2, extra={"big", "letter"}),
    }
    extras = [
        get_alphabet_choice("letter"),
        Choice("big", {
            "big": True,
        }),
    ]
    defaults = {
        "big": False,
    }


class AlphabetPlugin(Plugin):

    """Docstring for DictationPlugin. """

    _instance = None

    def __init__(self, name):
        """TODO: to be defined. """

        super().__init__(name)

    @staticmethod
    def get_rules():
        if AlphabetPlugin._instance is None:
            AlphabetPlugin._instance = CCRRule.create(Alphabet())
        return [AlphabetPlugin._instance]
