from dragonfly import FuncContext, Grammar
from mycastervoice import Plugin

from castertmux.tmux import Tmux
from castertmux.grammar import TmuxRule

def pane_cmd(tmux=None, check_value=None):
    # This context requires an check_value
    if check_value is None:
        return False

    _session = tmux._session

    pane = _session.attached_window.attached_pane

    pane_cmd = pane.get('pane_current_command')
    if pane_cmd == check_value:
        return True

    # try finding a child process which has check_value
    import subprocess
    ps = subprocess.Popen(['ps', '-a', '-o', 'pid,ppid,comm'], stdout=subprocess.PIPE, universal_newlines=True)
    ps.wait()
    processes = list(map(lambda row: row.split(), ps.communicate()[0].split('\n')[1:-1]))


    def find_child(pid):
        # Find if a process that has pid as parent
        for p in processes:
            if p[1] == pid:
                return p[0]
        return 0

    current_pid = pane.get('pane_pid')
    # Find all children
    while True:
        current_pid = find_child(current_pid)
        # No more children?
        if not current_pid:
            return False
        else:
            for p in processes:
                if p[0] == current_pid:
                    if p[2].split('/')[-1] == check_value:
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
