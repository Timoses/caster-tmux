from dragonfly import Grammar

from mycastervoice import Plugin
from mycastervoice.util.dragonfly import CCRRule

from mycasterplugin.dictation.alphabet import Alphabet
from mycasterplugin.dictation.control import Control
from mycasterplugin.dictation.format import Format
from mycasterplugin.dictation.punctuation import Punctuation

class DictationPlugin(Plugin):

    """Docstring for DictationPlugin. """

    def __init__(self):
        """TODO: to be defined. """

        super().__init__()

    def get_grammars(self):
        grammar = Grammar("Dictation")
        grammar.add_rule(CCRRule.create(
            Alphabet(),
            Punctuation(),
            Control(),
            Format(),
        ))
        return [grammar]
