class DefinitionFamily():
    '''This class defines a definition family. It has four members:
    _syntax: the synatic function, such as adj, prep, noun;
    _defintion: the definition of the word recorded in this family;
    _synonyms: all the synonyms corresponding to this definition;
    _antonyms: all the antonyms corresponding to this definition;


    '''

    def __init__(self):
        self._syntax = None
        self._definition = None

        self._synonyms = []
        self._antonyms = []

    def fill_syntax(self, syntax):
        self._syntax = syntax

    def fill_definition(self, definition):
        self._definition = definition

    def fill_synonyms(self, synonym):
        self._synonyms = synonym[:]

    def fill_antonyms(self, antonym):
        self._antonyms = antonym[:]

    def print_definition(self):
        print(self._definition)

    def print_syntax(self):
        print(self._syntax)

    def print_synonyms(self):
        print(self._synonyms)

    def print_antonyms(self):
        print(self._antonyms)


