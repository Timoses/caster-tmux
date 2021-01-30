from dragonfly import Repeat, Pause, Function, Choice, MappingRule, Dictation, IntegerRef, Context, Key

from enum import Enum

class Direction(Enum):
    LEFT = 'h'
    RIGHT = 'l'
    UP = 'k'
    DOWN = 'j'

from dragonfly import RecognitionObserver, RecognitionHistory
from six import integer_types
class RuleRecognitionHistory(list, RecognitionObserver):

    def __init__(self, length=10):
        list.__init__(self)
        RecognitionObserver.__init__(self)

        if (length is None or (isinstance(length, integer_types) and
                               length >= 1)):
            self._length = length
        else:
            raise ValueError("length must be a positive int or None,"
                             " received %r." % length)

    def on_recognition(self, words, rule, **kwargs):
        self.append((words, rule))
        if self._length:
            while len(self) > self._length:
                self.pop(0)

class RuleContext(Context):

    _rule_recognition_history = None

    def __init__(self, rule_class=None, rule_spec=None):
        if self._rule_recognition_history is None:
            RuleContext._rule_recognition_history = RuleRecognitionHistory()
            RuleContext._rule_recognition_history.register()

        self._rule_class = rule_class
        self._rule_spec = rule_spec

    def matches(self, executable, title, handle):
        if len(RuleContext._rule_recognition_history):
            previous = RuleContext._rule_recognition_history[-1]
            words = previous[0]
            rule = previous[1]
            if isinstance(rule, self._rule_class) and len(words) == 1 and words == tuple(self._rule_spec.split()):
                return True
        return False



def get_rules(emulate, prefix_letter, tmux=None):

    class TmuxRule(MappingRule):

        mapping = {
            "(window new)":
                Key('c-%s, c' % (prefix_letter)) if emulate
                else Function(tmux.window_new),
            "(window close)":
                Key('c-%s, &' % (prefix_letter)) if emulate
                else Function(tmux.window_close),
            "(window (<n>|last))":
                Key('c-%s, %(n)' % (prefix_letter)) if emulate
                else Function(tmux.window_n),
            "pane (<dir>|<n>)":
                Key('c-%s, %(dir)' % (prefix_letter)) if emulate
                else Function(tmux.pane_dir_n),
            "pane (zoom|unzoom)":
                Key('c-%s, z' % (prefix_letter)) if emulate
                else Function(tmux.pane_zoom),
            "pane new <dir> [full]":
                Function(tmux.pane_new),
            "pane close":
                Function(tmux.pane_close),
            "pane":
                Function(tmux.pane_display),
            "layout [(<layout>|even)]":
                Function(tmux.layout),
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
            Choice("dir", {
                    "lease": Direction.LEFT,
                    "left": Direction.LEFT,
                    "ross": Direction.RIGHT,
                    "right": Direction.RIGHT,
                    "dunce": Direction.DOWN,
                    "down": Direction.DOWN,
                    "sauce": Direction.UP,
                    "up": Direction.UP,
                }),
            IntegerRef("n", 0, 100),
            IntegerRef("m", 1, 10),
            Dictation("search"),
            Choice("layout", {
                    "horizontal|whore": "even-horizontal",
                    "vertical|virt": "even-vertical",
                    "tiled|tile": "tiled"
                }),
        ]
        defaults = {
                "n": 1,
                "m":"",
                "nth": ""
        }

#    class TmuxPane(MappingRule):
#        mapping = {
#            "<pane_number>": Function(tmux.pane_n)
#        }
#        context = RuleContext(TmuxRule, "pane")
#        extras = [
#            IntegerRef(name="pane_number", min=0, max=25)
#        ]

    return [TmuxRule()] #, TmuxPane()]
