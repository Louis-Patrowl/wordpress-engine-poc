import yaml
import regex
import sys

DIRECTORY = './test_directory/'
FINDERS_FILE = "dynamic_finders.yml"

# Regex contructor for ruby/regexp
def regex_constructor(loader: yaml.Loader, node: yaml.nodes.MappingNode) -> regex.Pattern:
    regex_string = loader.construct_scalar(node).lstrip("/")
    splitted_regex = regex_string.split('/')
    if splitted_regex[-1] == 'i':
        regex_string = regex_string[:-2]
        to_return = regex.compile(regex_string, regex.IGNORECASE)
    elif splitted_regex[-1] == 'mi':
        regex_string = regex_string[:-3]
        to_return = regex.compile(regex_string, regex.IGNORECASE | regex.MULTILINE)
    elif splitted_regex[-1] == '':
        regex_string = regex_string[:-1]
        to_return = regex.compile(regex_string)
    else:
        print('NOT IMPLEMENT REGEX: {regex_string}')
        sys.exit(0)
    return (to_return)

def load_dynamic_finders() -> dict:
    # Add a regex constructor for the yaml parser
    yaml.add_constructor('!ruby/regexp', regex_constructor)

    with open(DIRECTORY + FINDERS_FILE) as f:
        # Read the dynamic finders file and replace ruby regex with python regex
        replaced_regex = f.read().replace('(?<', '(?P<').replace(r'\z',r'\Z(?<!\n)').replace('^/', '')

        # Load yaml in a variable 
        dynamic_finders = yaml.load(replaced_regex, Loader=yaml.Loader)
    for i in dynamic_finders['plugins']:
        for j in dynamic_finders['plugins'][i]:
            if 'files' in dynamic_finders['plugins'][i][j]:
                dynamic_finders['plugins'][i][j]['files'] = [f"{i}/{x}" for x in dynamic_finders['plugins'][i][j]['files']]
    return (dynamic_finders)