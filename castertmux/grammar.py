from dragonfly import Repeat, Pause, Function, Choice, MappingRule, Dictation, IntegerRef

from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class TmuxRule(MappingRule):

    tmux = None

    def __init__(self, tmux):

        mapping = {
            "(window new)":
                Function(tmux.window_new),
            "(window close)":
                Function(tmux.window_close),
            "(window (<n>|last))":
                Function(tmux.window_n),
            "pane (<dir>|<n>)":
                Function(tmux.pane_dir_n),
            "pane (zoom|unzoom)":
                Function(tmux.pane_zoom),
            "pane new <dir> [full]":
                Function(tmux.pane_new),
            "pane close":
                Function(tmux.pane_close),
            "pane":
                Function(tmux.pane_display),
    #        "<n>":
    #            ContextSeeker([
    #                L(
    #                    S(["default"], NullAction()),
    #                    S(["pane_n"], Function(tmux.pane_n))
    #                )
    #            ]),
            "layout [(<layout>|even)]":
                Function(tmux.layout),
        }

        super().__init__(mapping=mapping)


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

