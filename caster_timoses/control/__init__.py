from dragonfly import MappingRule, Function, Grammar

from castervoice import Plugin
from castervoice.core import Controller

_plugin_name = None
_plugins_are_asleep = False
_sleeping_plugins = []

def sleep():
    global _plugin_name
    global _plugins_are_asleep
    global _sleeping_plugins

    if _plugins_are_asleep:
        return

    assert(len(_sleeping_plugins) == 0) # Ups, did I forget to wake someone?
    for plugin in Controller.get().plugin_manager.plugins:
        if plugin.name != _plugin_name:
            _sleeping_plugins.append(plugin)
            plugin.disable()

    _plugins_are_asleep = True

    # Wait until user presses a key
    #input()

def wake():
    global _plugin_name
    global _plugins_are_asleep
    global _sleeping_plugins

    if not _plugins_are_asleep:
        assert(len(_sleeping_plugins) == 0) # You shouldn't be asleep!

    while len(_sleeping_plugins):
        plugin = _sleeping_plugins[0]
        if plugin.name != _plugin_name:
            plugin.enable()
            _sleeping_plugins.remove(plugin)

    _plugins_are_asleep = False

class ControlRule(MappingRule):

    mapping = {
        "bye mike":
            Function(sleep),
        "hi mike":
            Function(wake)
    }
    extras = [
    ]
    defaults = {}


class ControlPlugin(Plugin):

    """Docstring for DictationPlugin. """

    def __init__(self, manager):
        """TODO: to be defined. """

        super().__init__(manager)
        global _plugin_name
        _plugin_name = self.name

    def get_grammars(self):
        grammar = Grammar(name="Control")
        grammar.add_rule(ControlRule())
        return [grammar]
