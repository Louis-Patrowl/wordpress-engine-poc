#!/usr/bin/python3

import sys
import regex
import argparse
import json
from termcolor import colored
import json
import colorama
from pymongo import MongoClient
import asyncio
from loader import load_wordpress_finders, load_plugin_finders
import os
from dotenv import load_dotenv
from test_time import testtime
import sqlite3

colorama.init()

from detection.wordpress import detect_wordpress
from detection.path import detect_path
from detection.version import detect_wordpress_version
from detection.plugins import detect_wordpress_plugins
from packaging.specifiers import SpecifierSet

from vulnerabilities import vulnerabilities_checker

from update import update_wordfence, update_wpscan, update_dynamic_finders

regex.DEFAULT_VERSION = regex.VERSION1



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
    MONGODB = os.getenv('MONGODB')
    db = MongoClient("mongodb://admin:password@localhost:27017/")  # Adjust the connection string as needed    
    return db


def load_fingerprints() -> dict:
    with open(DIRECTORY + FINGERPRINTS_FILE) as f:
        fingerprints = json.loads(f.read())
    return (fingerprints)

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
    load_dotenv()
    args = argument_parsing()
    
    print(args)

    db = connect_to_db()
    collection = db["wordpress_vulnerabilities"]["vulnerabilities"]  # Database name
    conn = sqlite3.connect(DIRECTORY + 'finders.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if args.update:
        update_wpscan()
        update_wordfence(collection)
        update_dynamic_finders(cursor)

    is_wordpress = await detect_wordpress(args)
    if is_wordpress == True:
        print(f"{args.URL} is a wordpress")
    else:
        print(f"{args.URL} is not a wordpress")
        sys.exit(0)
    content_dir = await detect_path(args)
    print(content_dir)
    time1 = testtime('finders wp')
    wordpress_finders = load_wordpress_finders()
    time1.end()
    time1 = testtime('finders wp')
    plugins_finder = load_plugin_finders()
    time1.end()
    time2 = testtime('metadata')
    metadata = load_metadata()
    time2.end()
    args.popular_plugins = [k for k, v in metadata['plugins'].items() if v['popular']]
    
    version_detection = await detect_wordpress_version(args, wordpress_finders)
    plugins_detection = await detect_wordpress_plugins(args, plugins_finder, content_dir)
    
    print(f"--- WP VERSION --- ")
    for i in version_detection:
        print(f"Wordpress {colored(i['version'], 'green')} detected by {colored(i['method'], 'light_blue')}")
    print(f"--- WP PLUGINS --- ")
    vulnerabilities_checker(plugins_detection, collection)

    db.close()
       

if __name__ == "__main__":
    #asyncio.run(main())
    load_dotenv()
    test1 = testtime('update')
    update_dynamic_finders()
    test1.end()

    DIRECTORY = os.getenv('DIRECTORY')


    test2 = testtime('wp')
    load_wordpress_finders(cursor)
    test2.end()
    test3 = testtime('plugins')
    load_plugin_finders(cursor)
    test3.end()
    conn.close()

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