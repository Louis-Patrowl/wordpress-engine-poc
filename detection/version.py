import httpx
import regex
from matchers.matcher_list import matcher_list

# TODO modify it with a dict that map class directly to name
async def find_and_match(args, finder, path = None, status = None):
    #print(finder['class'])
    if finder['class'] in matcher_list:
        to_find = matcher_list[finder['class']]( **finder)
    else:
        print(f"{finder['class']} not implemented yet")
        return False
    if await to_find.match(args.URL, path=path, status=status):
        print(f'Wordpress version found: {to_find.version}')
        return (to_find.version)
    return False

async def detect_wordpress_version(args, finders):
    print(f"--- WP VERSION --- ")
    to_return = []
    for i in finders:
        if 'path' in finders[i]: #TO Remove after testing
            continue
        detected = await find_and_match(args, finders[i])
        if detected:
            to_return.append({'method': f"{i} ({finders[i]['class']})", 'version': detected}) 
    if to_return and args.mode == "passive":
        return to_return
    
    #404
    for i in finders:
        if 'path' in finders[i]: #TO Remove after testing
            continue
        detected = await find_and_match(args, finders[i], path='ThisPageDoesntExistPatrowl', status=[404])
        if detected:
            to_return.append({'method': f"{i} (404) ({finders[i]['class']})", 'version': detected}) 
    return to_return