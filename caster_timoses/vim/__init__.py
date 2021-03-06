from castervoice import Plugin

from caster_timoses.vim.original.gvim import normalModeGrammar, insertModeBootstrap, commandModeBootstrap, insertModeGrammar, commandModeGrammar

class Vim(Plugin):

    def __init__(self, manager):
        super().__init__(manager)

    def get_grammars(self):
        return [normalModeGrammar, insertModeBootstrap, commandModeBootstrap]

    def get_context(self, desired_context=None):
        from dragonfly import FuncContext
        context = None
        if desired_context is None:
            return None
        elif "pane_cmd" in desired_context:
            defaults = {'tmux': self.tmux,
                        'check_value': desired_context["pane_cmd"]}
            context = FuncContext(pane_cmd, **defaults)

        return context

    def _apply_context(self, context=None):
        insertModeGrammar._context = context
        commandModeGrammar._context = context

    def load(self):
        Plugin.load(self)
        insertModeGrammar.load()
        commandModeGrammar.load()

    def enable(self):
        super().enable()
        insertModeGrammar.enable()
        commandModeGrammar.enable()

    def disable(self):
        super().disable()
        insertModeGrammar.disable()
        commandModeGrammar.disable()
