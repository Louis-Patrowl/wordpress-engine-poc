import httpx
import regex
from matchers.matcher_list import matcher_list

# TODO modify it with a dict that map class directly to name
def find_and_match(args, finder):
    print(finder['class'])
    if finder['class'] in matcher_list:
        to_find = matcher_list[finder['class']](**finder)
    else:
        print(f"{finder['class']} not implemented yet")
        return
    if to_find.match(args.URL, {}):
        print(f'Version found: {to_find.matched}')
        return True
    return False

def detect_wordpress_version(args, finders):
    for i in finders:
        print('-'*20)
        print(i)
        print('-'*20)
        find_and_match(args, finders[i])
