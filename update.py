import requests
import json
import os
import shutil
import sqlite3
from loader import load_dynamic_finders

def update_wordfence(collection):
    WORDFENCE_API = os.getenv('WORDFENCE_API')

    r = requests.get(WORDFENCE_API)
    data = json.loads(r.text)
    # MongoDB expects a list of documents for insertion
    documents = [value for key, value in data.items()]
    collection.delete_many({})
    collection.insert_many(documents)
    print(f"Inserted {len(documents)} documents into the collection.")

# Update all files needed using WPSCAN website
def update_wpscan():
    WPSCAN_DIRECTORY = os.getenv('WPSCAN_DIRECTORY')
    WPSCAN_API = os.getenv('WPSCAN_API')
    WPSCAN_FILES = [
        os.getenv('WPSCAN_FINGERPRINTS_FILE'),
        os.getenv('WPSCAN_FINDERS_FILE'),
        os.getenv('WPSCAN_METADATA_FILE')
    ] 

    if os.path.exists(WPSCAN_DIRECTORY):
        shutil.rmtree(WPSCAN_DIRECTORY)
    os.mkdir(WPSCAN_DIRECTORY)
    for file in WPSCAN_FILES:
        r = requests.get(WPSCAN_API + file)
        with open(WPSCAN_DIRECTORY + file, "wb") as f:
            f.write(r.content)

def update_dynamic_finders(cursor):
    cursor.execute("DROP TABLE IF EXISTS wordpress")
    #cursor.execute("DROP TABLE IF EXISTS themes")
    cursor.execute("DROP TABLE IF EXISTS plugins")

    # create wordpress finders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wordpress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class TEXT,
            xpath TEXT,
            pattern TEXT,
            version INTEGER,
            header TEXT,
            path TEXT,
            files TEXT,
            key TEXT
        )
    """)

    # create wordpress finders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plugins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plugin TEXT NOT NULL,
            name TEXT NOT NULL,
            class TEXT,
            xpath TEXT,
            pattern TEXT,
            version INTEGER,
            header TEXT,
            path TEXT,
            files TEXT,
            key TEXT
        )
    """)

    dynamic_finders = load_dynamic_finders()
    
    for wordpress_finder_name in dynamic_finders['wordpress']:
        finder = dynamic_finders['wordpress'][wordpress_finder_name]
        if 'path' in finder:
            if type(finder['path']) != list:
                path = [finder['path']]
            else:
                path = finder['path'] 
        else:
            path = None
        cursor.execute(
            "INSERT INTO wordpress (name, class, xpath, pattern, version, header, key, path, files) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                wordpress_finder_name,
                finder['class'],
                finder['xpath'] if 'xpath' in finder else None,
                finder['pattern'] if 'pattern' in finder else None,
                1 if 'version' in finder and finder['version'] == True else 0,
                finder['header'] if 'header' in finder else None,
                finder['key'] if 'key' in finder else None,
                ':$:'.join(path) if path else None,
                ':$:'.join(finder['files']) if 'files' in finder else None,
            )
        )

    for plugin_name in dynamic_finders['plugins']:
        for finder_name in dynamic_finders['plugins'][plugin_name]:
            finder = dynamic_finders['plugins'][plugin_name][finder_name]
            if 'path' in finder:
                if type(finder['path']) != list:
                    path = [finder['path']]
                else:
                    path = finder['path'] 
            else:
                path = None

            cursor.execute(
                "INSERT INTO plugins (plugin, name, class, xpath, pattern, version, header, key, path, files) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    plugin_name,
                    finder_name,
                    finder['class'] if 'class' in finder else None,
                    finder['xpath'] if 'xpath' in finder else None,
                    finder['pattern'] if 'pattern' in finder else None,
                    1 if 'version' in finder and finder['version'] == True else 0,
                    finder['header'] if 'header' in finder else None,
                    finder['key'] if 'key' in finder else None,
                    ':$:'.join(path) if path else None,
                    ':$:'.join(finder['files']) if 'files' in finder else None,
                )
            )