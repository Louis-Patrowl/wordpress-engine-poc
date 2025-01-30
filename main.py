#!/usr/bin/python3

import xml.etree
import requests
import os
import shutil
import yaml
import sys
import regex
from lxml import etree
import argparse
import json
import jmespath
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from colorama import init
from termcolor import colored
import json
from pymongo import MongoClient
import asyncio
init()

from detection.wordpress import detect_wordpress
from detection.path import detect_path
from detection.version import detect_wordpress_version
from detection.plugins import detect_wordpress_plugins

from vulnerabilies.vulnerabilities import vulnerabilities_checker

regex.DEFAULT_VERSION = regex.VERSION1

DIRECTORY = './test_directory/'

WPSCAN_API = "https://data.wpscan.org/"

WORDFENCE_API = "https://www.wordfence.com/api/intelligence/v2/vulnerabilities/production"
FINGERPRINTS_FILE = "wp_fingerprints.json"
FINDERS_FILE = "dynamic_finders.yml"
METADATA_FILE = "metadata.json"
WPSCAN_FILES = [FINGERPRINTS_FILE, FINDERS_FILE, METADATA_FILE] 

from_version = '*'
from_inclusive = True
to_version = '5.9'
to_inclusive = True

def get_version_range(version):
    # Constructing the specifier string
    for i in version:
        version = version[i]
        break
    specifier = ""

    # Handling the lower bound

    if version['from_version'] == '*':
        specifier += ""
    elif version['from_inclusive']:
        specifier += f">={version['from_version']}"
    else:
        specifier += f">{version['from_version']}"
    # Handling the upper bound
    if version['to_inclusive']:
        specifier += f",<={version['to_version']}"
    else:
        specifier += f",<{version['to_version']}"
    return SpecifierSet(specifier)

def connect_to_db():
    client = MongoClient("mongodb://admin:password@localhost:27017/")  # Adjust the connection string as needed
    db = client["wordpress_vulnerabilities"]  # Database name
    collection = db["vulnerabilities"]  # Collection name
    return collection

def initialize_db(collection):
    r = requests.get(WORDFENCE_API)
    #print(r.text)
    data = json.loads(r.text)
    # MongoDB expects a list of documents for insertion
    documents = [value for key, value in data.items()]
    collection.insert_many(documents)
    print(f"Inserted {len(documents)} documents into the collection.")



# Update all files needed using WPSCAN website
def update_db():
    if os.path.exists(DIRECTORY):
        shutil.rmtree(DIRECTORY)
    os.mkdir(DIRECTORY)
    for i in WPSCAN_FILES:
        r = requests.get(WPSCAN_API + i)
        with open(DIRECTORY + i, "wb") as f:
            f.write(r.content)

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

def load_fingerprints() -> dict:
    with open(DIRECTORY + FINGERPRINTS_FILE) as f:
        fingerprints = json.loads(f.read())
    return (fingerprints)


# Load dynamic finders in a dict from WPSCAN db file
def load_dynamic_finders() -> dict:
    # Add a regex constructor for the yaml parser
    yaml.add_constructor('!ruby/regexp', regex_constructor)

    with open(DIRECTORY + FINDERS_FILE) as f:
        # Read the dynamic finders file and replace ruby regex with python regex
        replaced_regex = f.read().replace('(?<', '(?P<').replace(r'\z',r'\Z(?<!\n)').replace('^/', '')

        # Load yaml in a variable 
        dynamic_finders = yaml.load(replaced_regex, Loader=yaml.Loader)
    return (dynamic_finders)

def load_metadata():
    with open("./test_directory/metadata.json") as f:
        metadata = json.loads(f.read())
        return (metadata)

def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some inputs.")
    parser.add_argument(
        "--update",
        action="store_true",
        help="If specified, set the update flag to True."
    )
 #   parser.add_argument(
 #       "--fingerprint",
 #       action="store_true",
 #       help="If specified, set the update flag to True."
 #   )    
 #   parser.add_argument(
 #       "--wp-version",
 #       action="store_true",
 #       help="If specified, set the update flag to True."
 #   )
 #   parser.add_argument(
 #       "--plugins",
 #       action="store_true",
 #       help="If specified, set the update flag to True."
 #   )
 #   parser.add_argument(
 #       "--theme",
 #       action="store_true",
 #       help="If specified, set the update flag to True."
 #   )    
    parser.add_argument(
        "-m", "--mode",
        choices=["passive", "aggressive", "mixed"],
        default="mixed",
        help="Specify the mode ('mixed' by default)",
    )
    parser.add_argument(
        "URL",
        help="The mandatory URL argument."
    )

    args = parser.parse_args()
    if args.URL[-1] != '/':
        args.URL += '/'
    
    return (args)


def do_something(truc):
    print(truc)


async def main():
    args = argument_parsing()
    print(args)

    if args.update:
        update_db()

    is_wordpress = await detect_wordpress(args)
    if is_wordpress == True:
        print(f"{args.URL} is a wordpress")
    else:
        print(f"{args.URL} is not a wordpress")
        sys.exit(0)
    content_dir = await detect_path(args)
    print(content_dir)
    dynamic_finders = load_dynamic_finders()
    metadata = load_metadata()
    args.popular_plugins = [k for k, v in metadata['plugins'].items() if v['popular']]
    
    version_detection = await detect_wordpress_version(args, dynamic_finders['wordpress'])
    plugins_detection = await detect_wordpress_plugins(args, dynamic_finders['plugins'], content_dir)
    collection = connect_to_db()
    collection.delete_many({})
    initialize_db(collection)
    print(f"--- WP VERSION --- ")
    for i in version_detection:
        print(f"Wordpress {colored(i['version'], 'green')} detected by {colored(i['method'], 'light_blue')}")
    print(f"--- WP PLUGINS --- ")
    vulnerabilities_checker(plugins_detection, collection)
       

if __name__ == "__main__":
    asyncio.run(main())

    #if args.fingerprint:
    #    fingerprints = load_fingerprints()
    #    print(fingerprints_wp_version(fingerprints, args.mode))
    #dynamic_finders = load_dynamic_finders()


    #do_something(dynamic_finders)
#
    ##r = requests.get(sys.argv[2])
    ##tree = etree.fromstring(r.content, etree.HTMLParser())
#
    ##print(tree.xpath('//meta[@name="generator"]/@content'))
    ##print(dynamic_finders['wordpress'])