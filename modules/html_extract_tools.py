import sys
import tempfile
import re
# here because python3 and python2 have different url package structure.
# and also different builtin open function call signatures
if sys.version_info[0] >= 3:
    import urllib.request
    common_urlretrieve = urllib.request.urlretrieve
elif sys.version_info[0] <= 2:
    import urllib
    common_urlretrieve = urllib.urlretrieve
    import io


def save_retrieved_html(word):
    '''This function retrieves the html page for the word "word",
    then save the file to a temporary file. The file name will
    be returned at the end.
    '''

    url = 'http://www.thesaurus.com/browse/' + word + '?s=t'
    temp_file_name = tempfile.mktemp()
    try:
        common_urlretrieve(url, temp_file_name)
        return temp_file_name
    except:
        return None


def extract_definition_line(tem_file_name):
    '''This function opens the webpage file stored previously using the
    function save_retrieved_html(). Then it looks for the line containing
    all the definitions, synonyms and antonyms. These explanation is stored
    soley within one super long line. This function returns this long line using
    a string object
    '''
    # the following is because the builtin open function in python2
    # does not support encoding parameter. use io.open instead. But
    # io.open().readline() returns the UNICODE STRING reprsentation of
    # each character. Therefore you need to encode it using utf-8
    if sys.version_info[0] <= 2:
        with io.open(tem_file_name, 'r', encoding='utf-8') as f:
            line = f.readline().encode('utf-8')
            while line != '':
                line1 = line.lstrip()
                line2 = line1.rstrip()
                if (line2[0:28] == '<script>window.INITIAL_STATE'):
                    definition_line = line2
                    break
                line = f.readline().encode('utf-8')

            f.close()

    else:
        with open(tem_file_name, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line != '':
                line1 = line.lstrip()
                line2 = line1.rstrip()
                if (line2[0:28] == '<script>window.INITIAL_STATE'):
                    definition_line = line2
                    break
                line = f.readline()

            f.close()

    return definition_line


def split_definition_groups(definition_line):
    ''''This function splits the super long definition line into a list of
    strings, each of which is a definition group. It contains its explanation,
    synatic function, synonyms and antonyms. Each group has the following format

    {"isInformal": null, ... definition: "very great",...
    "pos", ajd", "synonyms": [{"similarity":"100", ..."targetTerm": "acute"...}{}{}...{}],
    "antonyms": [{"similarity":"-100", ...TargetTerm: "calm",...},{},{}....{}],"note":null}

    Note the above group is a one-line string when returned as list member

    The call signature is

    split_definition_groups(definition_line)

    and it returns a list of strings.
    '''
    return re.findall(r"{\"isInformal\":.*?}\],\"note\":null}", definition_line)
    "note here we need to use non-greedy .*? arbitrary matches"


def extract_pair_values_via_key(str, key, value_quote_type):
    '''This function extracts the value from the string input of the form
    r{"key1": "value1", "key2":"value2"...} (note this is the literal
    content, not a python dictionary) via specifying the key and
    the quote type of the corresponding value. The output strips the quotes
    of the value. But the key must be indential to the that appeared in the
    original input string.
    Its call signature is

    extract_pair_values_by_key(str, key, value_quote_type)
    # str: input str such as {"key1": "value1", "key2":"value2"...},
    # key: key string such as '"key1"'.
    # value_quote_type: such has '"' or r'['

    # Note here you need to # put quotes around key1 because
    # it is inside the string. However, for convenience,
    # the output values will have their quotes stripped away.


    Note if multiple pairs having the same key, it returns a list of values,
    each member of which is a string. Otherwise it still return a list but
    the length of which is one.
    '''

    # first find all the pairs with the key
    if (value_quote_type == '"'):
        re_search_str = key + r':"(.*?)"'
    elif (value_quote_type == '['):
        re_search_str = key + r':\[(.*?)\]'

    occured_pairs = re.findall(re_search_str, str)
    values = []
    for each_pair in occured_pairs:
        values.append(re.sub(re_search_str, r'\r', each_pair))

    return values


def parse_group(explanation_group, type=None):
    '''This function parses a single splitted explanation group. It deprives
    all other useless information and only retrain the request results

    Its call signature is:

    parse_group(group)  # return a string for its definition
    parse_group(group, [type=]'definition') # return a str for its def
    parse_group(group, [type=]'syntax') # return a str for its syntax
    parse_group(group, [type=]'synonym') # return a list of its synonyms
    parse_group(group, [type=]'antonym') # return a list of its antonyms

    '''
    if (type == None or type == 'definition'):
        definition_list = extract_pair_values_via_key(
            explanation_group, '"definition"', '"')
        return definition_list[0]
    elif (type == 'syntax'):
        syntax_list = extract_pair_values_via_key(explanation_group,
                                                  '"pos"', '"')
        return syntax_list[0]
    elif (type == 'synonym'):
        # from "synonyms":[{}{}{}]
        synonyms_value_list = extract_pair_values_via_key(
            explanation_group, '"synonyms"', '[')
        entire_synonyms_block = synonyms_value_list[0]
        # now we have got the long string {}{}{}{}, each of which is a
        # block of the form {"similarity":"100", targetTerm":"high",...}
        # let us now extract the target words from each block simutaneously
        synonym_list = extract_pair_values_via_key(entire_synonyms_block,
                                                   '"targetTerm"', '"')
        return synonym_list

    elif (type == 'antonym'):
        antonyms_value_list = extract_pair_values_via_key(
            explanation_group, '"antonyms"', '[')
        entire_antonyms_block = antonyms_value_list[0]
        # now we have got the long string {}{}{}{}, each of which is a
        # block of the form {"similarity":"100", targetTerm":"high",...}
        # let us now extract the target words from each block simutaneously
        antonym_list = extract_pair_values_via_key(entire_antonyms_block,
                                                   '"targetTerm"', '"')
        return antonym_list
    else:
        print('Error, unexpected request types')
        return None

