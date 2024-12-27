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

from detection.wordpress import detect_wordpress
from detection.version import detect_wordpress_version
from detection.plugins import detect_wordpress_plugins

regex.DEFAULT_VERSION = regex.VERSION1

DIRECTORY = './test_directory/'

WPSCAN_API = "https://data.wpscan.org/"

FINGERPRINTS_FILE = "wp_fingerprints.json"
FINDERS_FILE = "dynamic_finders.yml"
WPSCAN_FILES = [FINGERPRINTS_FILE, FINDERS_FILE] 


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
    
    if regex_string[-3:] != r'\/i' and regex_string[-2:] == '/i':
        regex_string = regex_string[:-2]
    elif regex_string[-2:] != r'\/' and regex_string[-1:] == '/':
        regex_string = regex_string[:-1]
    
    return (regex.compile(regex_string, regex.IGNORECASE))

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
 #   parser.add_argument(
 #       "-m", "--mode",
 #       choices=["passive", "aggressive"],
 #       default="passive",
 #       help="Specify the mode ('passive' by default)",
 #   )
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

args = argument_parsing()

is_wordpress = detect_wordpress(args)
if is_wordpress == True:
    print(f"{args.URL} is a wordpress")

dynamic_finders = load_dynamic_finders()
#do_something(dynamic_finders)

#detect_wordpress_version(args, dynamic_finders['wordpress'])
detect_wordpress_plugins(args, dynamic_finders['plugins'])
#if args.fingerprint:
#    fingerprints = load_fingerprints()
#    print(fingerprints_wp_version(fingerprints, args.mode))
#dynamic_finders = load_dynamic_finders()


#do_something(dynamic_finders)

#r = requests.get(sys.argv[2])
#tree = etree.fromstring(r.content, etree.HTMLParser())

#print(tree.xpath('//meta[@name="generator"]/@content'))
#print(dynamic_finders['wordpress'])