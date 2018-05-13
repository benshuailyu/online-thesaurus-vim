'''This program defines a function online_thesaurus()
to find the synonyms and antonyms of a given word. 
The function syntax is

online_thesaurus(word)

where word is a string specifying the request word and
the return value is a list of definition families. 
A definition family is a class representing the definition, 
synonyms and antonyms etc of a particluar meaning

'''

__DEBUG__ =  0
from DefinitionFamily import *
from htmlExtract import *


def online_thesaurus(word):
    html_fname = save_retrieved_html(word)
    super_long_definition_line = extract_definition_line(html_fname)
    definition_group_list = split_definition_groups(
        super_long_definition_line
    )

    thesuarus_list = []
    for each_definition_group in definition_group_list:
        new_family = DefinitionFamily()
        new_family.fill_definition(parse_group(
            each_definition_group, 'definition'))
        new_family.fill_syntax(parse_group(each_definition_group, 'syntax'))
        new_family.fill_synonyms(parse_group(each_definition_group, 'synonym'))
        new_family.fill_antonyms(parse_group(each_definition_group, 'antonym'))
        thesuarus_list.append(new_family)

    if __DEBUG__ == 1:
        for ai in thesuarus_list:
            ai.print_definition()
            ai.print_syntax()
            ai.print_synonyms()
            ai.print_antonyms()

    return thesuarus_list

online_thesaurus("new")

