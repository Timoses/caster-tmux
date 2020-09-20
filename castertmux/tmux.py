from libtmux import Server

from castertmux.grammar import Direction

class Tmux(object):
    _server  = None
    _session = None

    """Docstring for Tmux. """

    def __init__(self):
        """TODO: to be defined. """
        self._server = Server()
        self._session = self._server.sessions[0]

    def window_new(self):
        self._session.new_window()

    def window_close(self):
        self._session.attached_window.kill_window()

    def window_n(self, **defaults):
        self._session.select_window(defaults['n'])

    def pane_display(self):
        self._server.cmd('display-panes', '-d1000')

    def pane_dir_n(self, **defaults):
        if 'dir' in defaults:
            dir_options = {
                Direction.UP: "-U",
                Direction.DOWN: "-D",
                Direction.LEFT: "-L",
                Direction.RIGHT: "-R"
            }

            self._session.attached_window.select_pane(dir_options[defaults['dir']])
        else:
            self._session.attached_window.select_pane(defaults['n'])

    def pane_n(self, pane_number):
        self._session.attached_window.select_pane(pane_number)

    def pane_zoom(self):
        self._session.attached_window.attached_pane.cmd('resize-pane', '-Z')

    def pane_new(self, dir, _node):
        args = "-"
        dir_options = {
            Direction.UP: "vb",
            Direction.DOWN: "v",
            Direction.LEFT: "hb",
            Direction.RIGHT: "h"
        }

        args = args + dir_options[dir]

        if _node.results[-1][0] == 'full':
            args += "f"

        # open pane in same directory
        current_path = self._session.attached_window.attached_pane.get('pane_current_path')
        args = [args, '-c', current_path]

        self._session.attached_window.cmd('split-window', *args)


    def pane_close(self):
        self._session.attached_window.attached_pane.cmd('kill-pane')

    def layout(self, _node, layout=None):
        if _node.results[-1][0] == 'even':
            self._session.attached_window.cmd('select-layout', '-E')
        else:
            self._session.attached_window.cmd('select-layout', layout)


