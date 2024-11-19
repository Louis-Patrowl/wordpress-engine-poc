#!/usr/bin/python3

import requests
import os
import shutil
import yaml
import sys
import regex

regex.DEFAULT_VERSION = regex.VERSION1

DIRECTORY = './test_directory/'

WPSCAN_API = "https://data.wpscan.org/"

WP_VERSION_FILE = "wp_fingerprints.json"
FINGERPRINT_DB = "dynamic_finders.yml"
WPSCAN_FILES = [WP_VERSION_FILE, FINGERPRINT_DB] 

def get_files():
    if os.path.exists(DIRECTORY):
        shutil.rmtree(DIRECTORY)
    os.mkdir(DIRECTORY)
    for i in WPSCAN_FILES:
        r = requests.get(WPSCAN_API + i)
        with open(DIRECTORY + i, "wb") as f:
            f.write(r.content)

def test_contructor(loader, node):
    print(node)
    return regex.compile(loader.construct_scalar(node))

def load_df():
    yaml.add_constructor('!ruby/regexp', test_contructor)
    with open(DIRECTORY + FINGERPRINT_DB) as f:
        to_replace = f.read().replace('(?<', '(?P<').replace(r'\z',r'\Z(?<!\n)')
        to_return = yaml.load(to_replace, Loader=yaml.Loader)
    return (to_return)

if sys.argv[1] == 'update':
    get_files()
dynamic_finders = load_df()
print(dynamic_finders['wordpress'])