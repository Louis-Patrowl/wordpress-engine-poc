import requests
import json
import os
import shutil

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