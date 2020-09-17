from dragonfly import FuncContext, Grammar
from mycastervoice import Plugin

from castertmux.tmux import Tmux
from castertmux.grammar import TmuxRule

def pane_cmd(tmux=None, check_value=None):
    # This context requires an check_value
    if check_value is None:
        return False

    _session = tmux._session

    # most often the shell
    pane_parent_pid = _session.attached_window.attached_pane.get('pane_pid')
    print(_session.attached_window.attached_pane.values())
    import subprocess
    ps = subprocess.Popen(['ps', '-a', '-o', 'ppid,comm'], stdout=subprocess.PIPE, universal_newlines=True)
    ps.wait()
    stdout, _O = ps.communicate()
    if stdout is None:
        return False
    for row in stdout.split('\n'):
        splits = row.strip().split(' ')
        # Is the process running in in the parent shell
        # of the current pane?
        if splits[0] == pane_parent_pid:
            command_name = splits[1].split('/')[-1]
            if command_name == check_value:
                return True

class TmuxPlugin(Plugin):

    _grammar = None

    def __init__(self):

        self.tmux = Tmux()
        super().__init__()

    def get_grammars(self):
        if TmuxPlugin._grammar is None:
            TmuxPlugin._grammar = Grammar("Tmux")
            TmuxPlugin._grammar.add_rule(TmuxRule(self.tmux))
        return [TmuxPlugin._grammar]

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
