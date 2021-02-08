from getpass import getpass

from pykeepass import PyKeePass

from dragonfly import MappingRule, Grammar, Text, Key

from castervoice import Plugin




class KeepassPlugin(Plugin):

    kp = None

    def __init__(self, manager):

        super().__init__(manager)

        db_path = self.config['path']

        # Since Caster does not provide any encrypted state or config
        # we ask the user for his password on every initialization
        db_pw = getpass("Keepass - Enter password for DB %s: " % db_path)
        self.kp = PyKeePass(db_path, password=db_pw)

        self.entries = {}

        for entry in self.kp.find_entries_by_notes('castervoice:.*', regex=True):
            notes = entry.notes.splitlines()
            for note in notes:
                if note.startswith('castervoice: '):
                    self.entries.update({note.replace('castervoice: ', ''): entry})

    def get_grammars(self):

        mapping = {}
        for words, entry in self.entries.items():
            mapping.update({'key pass ' + words: Text(entry.password)})
            mapping.update({'key user ' + words: Text(entry.username)})
            mapping.update({'key tab ' + words: Text(entry.username) + Key('tab') + Text(entry.password)})

        rule = MappingRule(mapping=mapping)
        grammar = Grammar(name="Keepass")
        grammar.add_rule(rule)
        return [grammar]
