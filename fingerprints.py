import httpx
import hashlib

FINGERPRINTS_PASSIVE_PATH = ['/']


def fingerprints_wp_version(fingerprints: dict, args: dict):
    possible_versions = {}

    if args.mode == "passive":
        return
    for i in fingerprints:
        possible_versions[i] = []
        response = httpx.get(args.url + i)
        
        md5sum = hashlib.md5(response.text).hexdigest()
        if md5sum in fingerprints[i]:
            possible_versions[i] += fingerprints[i]