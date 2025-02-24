import yaml
import regex
import sys


DIRECTORY = './test_directory/'
FINDERS_FILE = "dynamic_finders.yml"

# Regex contructor for ruby/regexp
def regex_constructor(loader: yaml.Loader, node: yaml.nodes.MappingNode):# -> regex.Pattern:
    regex_string = loader.construct_scalar(node).lstrip("/")
    return (regex_string)


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


def pattern_to_regex(regex_string: str):
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

def load_wordpress_finders(cursor) -> dict:
    to_return = {}

    cursor.execute("SELECT * FROM wordpress")
    rows = cursor.fetchall()

    for row in rows:
        to_return[row['name']] =  {
            'class': row['class'] if row['class'] else None,
            'xpath': row['xpath'] if row['xpath'] else None,
            'pattern': pattern_to_regex(row['pattern']) if row['pattern'] else None,
            'version': row['version'] if row['version'] else None,
            'header': row['header'] if row['header'] else None,
            'path': row['path'] if row['path'] else None,
            'files': row['files'] if row['files'] else None,
            'key': row['key'] if row['key'] else None,
        }
    return to_return

def load_plugin_finders(cursor) -> dict:
    to_return = {}
    cursor.execute("SELECT * FROM plugins")
    rows = cursor.fetchall()
    for row in rows:
        if row['plugin'] not in to_return:
            to_return[row['plugin']] = {}
        to_return[row['plugin']][row['name']] = {
            'class': row['class'] if row['class'] else None,
            'xpath': row['xpath'] if row['xpath'] else None,
            'pattern': pattern_to_regex(row['pattern']) if row['pattern'] else None,
            'version': row['version'] if row['version'] else None,
            'header': row['header'] if row['header'] else None,
            'path': row['path'] if row['path'] in row else None,
            'files': row['files'] if row['files'] in row else None,
            'key': row['key'] if row['key'] in row else None,
        }
    return to_return