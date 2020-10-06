from dragonfly import MappingRule, Text, Key, Grammar

from castervoice import Plugin


class GitRule(MappingRule):

    mapping = {
        "git diff":
            Text("git diff") + Key("enter"),
        "git diff cached":
            Text("git diff --cached") + Key("enter"),
        "git show":
            Text("git show") + Key("enter"),
        "git commit":
            Text("git commit") + Key("enter"),
        "git commit amend":
            Text("git commit --amend") + Key("enter"),
        "git add partial":
            Text("git add -p") + Key("enter"),
        "git rebase interactive":
            Text("git rebase -i HEAD~"),
        "git rebase continue":
            Text("git rebase --continue"),
        "git reset hard":
            Text("git reset --hard"),
        "git fetch [all]":
            Text("git fetch --all") + Key("enter"),
        "git a log":
            Text("git alog") + Key("enter"),
        "git status":
            Text("git status") + Key("enter"),
        "git push sys":
            Text("git push hss $(git rev-parse --abbrev-ref HEAD)") + Key("enter"),
        "git tag":
            Text("git tag "),
        "(git add partial)":
            Text("git add -p") + Key("enter"),
        "git push":
            Text("git push "),
    }
    extras = [
    ]
    defaults = {}

class GitPlugin(Plugin):

    """Docstring for DictationPlugin. """

    def __init__(self, manager):
        """TODO: to be defined. """

        super().__init__(manager)

    def get_grammars(self):
        grammar = Grammar(name="Git")
        grammar.add_rule(GitRule())
        return [grammar]
