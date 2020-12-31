from dragonfly import Repeat, Pause, Function, Choice, MappingRule, Dictation, IntegerRef, Key, Text, Grammar

from castervoice import Plugin


class FirefoxRule(MappingRule):
    mapping = {
        "(new window|window new)":
            Key("w-n"),
        "(new incognito window | incognito)":
            Key("ws-p"),
        "window close|close all tabs":
            Key("cs-w"),
        "new tab [<n>]|tab new [<n>]":
            Key("w-t") * Repeat(extra="n"),
        "reopen tab [<n>]|tab reopen [<n>]":
            Key("ws-t") * Repeat(extra="n"),
        "(back|previous) tab [<n>]|tab (left|lease) [<n>]":
            Key("cs-tab") * Repeat(extra="n"),
        "(next|forward) tab [<n>]|tab (right|sauce) [<n>]":
            Key("c-tab") * Repeat(extra="n"),
        "close tab [<n>]|tab close [<n>]":
            Key("w-w") * Repeat(extra='n'),
        "go (back|prev|prior|previous) [<n>]":
            Key("w-left/20") * Repeat(extra="n"),
        "go (next|forward) [<n>]":
            Key("w-right/20") * Repeat(extra="n"),
        "find (next|forward) [match] [<n>]":
            Key("w-g/20") * Repeat(extra="n"),

        "find <search>":
            Key("w-f/20") + Text("%(search)s"),
        "search <search>":
            Key("w-l/20") + Text("%(search)s")
    }
    extras = [
        Choice("nth", {
                "first": "1",
                "second": "2",
                "third": "3",
                "fourth": "4",
                "fifth": "5",
                "sixth": "6",
                "seventh": "7",
                "eighth": "8",
            }),
        IntegerRef("n", 1, 100),
        IntegerRef("m", 1, 10),
        Dictation("search")
    ]
    defaults = {"n": 1, "m": "", "nth": ""}


class FirefoxPlugin(Plugin):

    """Docstring for DictationPlugin. """

    def __init__(self, manager):
        """TODO: to be defined. """

        super().__init__(manager)

    def get_grammars(self):
        grammar = Grammar(name="Git")
        grammar.add_rule(FirefoxRule())
        return [grammar]
