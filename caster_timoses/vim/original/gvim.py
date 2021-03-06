# Try remote debugging
# import ptvsd
# ptvsd.enable_attach("", address = ('127.0.0.1', 3000))
# ptvsd.wait_for_attach()

from dragonfly import *
from caster_timoses.vim.original.rules import action, motion, object, navigation, buffer, quick_replace, quick_settings, diff, general
from caster_timoses.vim.original.plugins import surround, easy_motion, netrw, ctrlp, fugitive, unimpaired, snipmate, deoplete
from caster_timoses.vim.original.vim_config import get_config
#from libtmux import Server
#try:
#    import pkg_resources
#    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
#except ImportError:
#    pass

print('new gVim grammar accessed.')

# Saving generally useful info
config = get_config()
release = Key("shift:up, ctrl:up")

### 1. Normal mode
# a. What rules go in the chainable continuous command recognition?
normal_CCR_rules = [
    RuleRef(rule = action.ActionRule()),
    RuleRef(rule = motion.MotionRule()),
    #RuleRef(rule = surround.SurroundRule()),
    RuleRef(rule = diff.DiffRule()),
    #RuleRef(rule = unimpaired.UnimpairedRule()),
    RuleRef(rule = general.GeneralRule()),
]

normal_CCR = Repetition(Alternative(normal_CCR_rules),
                        min = 1, max = 10,
                        name = "normal_mode_sequence")

class NormalModeCCR(CompoundRule):
    spec     = "<normal_mode_sequence>"
    extras   = [ normal_CCR ]
    def _process_recognition(self, node, extras):
        # A sequence of actions.
        normal_mode_sequence = extras["normal_mode_sequence"]
        # An integer repeat count.
        for action in normal_mode_sequence:
            action.execute()
        release.execute()

# b. What rules should not be chainable?
normal_single_rules = [
    #RuleRef(rule = easy_motion.EasyMotionRule()),
    RuleRef(rule = navigation.NavigationRule()),
    RuleRef(rule = netrw.NetrwRule()),
    #RuleRef(rule = ctrlp.CtrlPRule()),
    RuleRef(rule = buffer.BufferRule()),
    RuleRef(rule = quick_replace.QuickReplaceRule()),
    RuleRef(rule = quick_settings.QuickSettingsRule()),
    #RuleRef(rule = fugitive.FugitiveRule()),
]
normal_single_action = Alternative(normal_single_rules, name = "normal_mode_single_action")

class NormalModeSingleAction(CompoundRule):
    spec = "<normal_mode_single_action>"
    extras = [ normal_single_action ]
    def _process_recognition(self, node, extras):
        action = extras["normal_mode_single_action"]
        action.execute()
        release.execute()

### 2. Insert mode
from caster_timoses.vim.original.rules.insert_mode import InsertModeStartRule, InsertModeFinishRule
from caster_timoses.vim.original.rules.insert_mode import InsertModeCommands, InsertModeCCR
# create continuous resolution for insert mode, too

# Inherit all mappings, extras, defaults from InsertModeStartRule
class InsertModeEnabler(InsertModeStartRule):
    def _process_recognition(self, node, extras):
        insertModeBootstrap.disable()
        normalModeGrammar.disable()
        insertModeGrammar.enable()
        # Note: there are issues with the super call. If you run into them,
        # do not fret and google for super TypeError order.
        super(self.__class__, self)._process_recognition(node, extras)
        print("\n(INSERT)")

class InsertModeDisabler(InsertModeFinishRule):
    def _process_recognition(self, node, extras):
        insertModeGrammar.disable()
        insertModeBootstrap.enable()
        normalModeGrammar.enable()
        super(self.__class__, self)._process_recognition(node, extras)
        print("\n(NORMAL)")

### 3. Command mode
from caster_timoses.vim.original.rules.command_mode import CommandModeStartRule, CommandModeFinishRule, CommandModeCommands

class CommandModeEnabler(CommandModeStartRule):
    def _process_recognition(self, node, extras):
        commandModeBootstrap.disable()
        normalModeGrammar.disable()
        commandModeGrammar.enable()
        super(self.__class__, self)._process_recognition(node, extras)
        print("\n(EX MODE)")

class CommandModeDisabler(CommandModeFinishRule):
    def _process_recognition(self, node, extras):
        commandModeGrammar.disable()
        commandModeBootstrap.enable()
        normalModeGrammar.enable()
        super(self.__class__, self)._process_recognition(node, extras)
        print("\n(NORMAL)")

### 4. Prep & activate the requisite grammars
#def is_vim():
#    _server = Server()
#    _session = _server.sessions[0]
#    # most often the shell
#    pane_parent_pid = _session.attached_window.attached_pane.get('pane_pid')
#    import subprocess
#    ps = subprocess.Popen(['ps', '-a', '-o', 'ppid,comm'], stdout=subprocess.PIPE, universal_newlines=True)
#    ps.wait()
#    stdout, _O = ps.communicate()
#    if stdout is None:
#        return False
#    for row in stdout.split('\n'):
#        splits = row.strip().split(' ')
#        # Is the process running in in the parent shell
#        # of the current pane?
#        if splits[0] == pane_parent_pid:
#            if splits[1] == 'nvim':
#                return True
#terminal_context = AppContext(executable="alacritty")
#vim_context = FuncContext(is_vim)
#
#gvim_context = (terminal_context & vim_context)

gvim_context = None

# a. Normal mode - on by default
normalModeGrammar = Grammar("gvim", context=gvim_context)
normalModeGrammar.add_rule(NormalModeCCR())
normalModeGrammar.add_rule(NormalModeSingleAction())
#normalModeGrammar.load()

# b. Insert and Command modes - waiting for activation
# Bootstrap = insert-mode activating set of rules
insertModeBootstrap = Grammar("Insert Mode bootstrap", context=gvim_context)
insertModeBootstrap.add_rule(InsertModeEnabler())
#insertModeBootstrap.load()

# Grammar = set of commands in the actual mode, when invoked by bootstrap
insertModeGrammar = Grammar("Insert Mode grammar", context=gvim_context)
# insertModeGrammar.add_rule(InsertModeCCR())
insertModeGrammar.add_rule(InsertModeCommands())
insertModeGrammar.add_rule(InsertModeDisabler())
#insertModeGrammar.add_rule(snipmate.SnipMateRule())
insertModeGrammar.add_rule(deoplete.DeopleteRule())
#insertModeGrammar.load()
#insertModeGrammar.disable()

# same for command mode
commandModeBootstrap = Grammar("Command Mode bootstrap", context=gvim_context)
commandModeBootstrap.add_rule(CommandModeEnabler())
#commandModeBootstrap.load()

commandModeGrammar = Grammar("Command Mode grammar", context=gvim_context)
commandModeGrammar.add_rule(CommandModeCommands())
commandModeGrammar.add_rule(CommandModeDisabler())
#commandModeGrammar.load()
#commandModeGrammar.disable()

# Unload function which will be called at unload time
def unload():
    global normalModeGrammar
    if normalModeGrammar: normalModeGrammar.unload()
    normalModeGrammar = None

    global commandModeGrammar
    if commandModeGrammar: commandModeGrammar.unload()
    commandModeGrammar = None

    global insertModeGrammar
    if insertModeGrammar: insertModeGrammar.unload()
    insertModeGrammar = None
