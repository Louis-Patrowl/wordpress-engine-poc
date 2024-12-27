import httpx
import regex
from matchers.matcher_list import matcher_list

# TODO modify it with a dict that map class directly to name
def find_and_match(args, finder, plugin, name):
    print(f"{plugin}: {name}")
    if name == 'Readme':
        to_find = matcher_list['BodyPattern'](**finder)
    elif name == 'QueryParameter':
        to_find = matcher_list['QueryParameter'](**finder)
    elif finder['class'] in matcher_list:
        to_find = matcher_list[finder['class']](**finder)
    else:
        print(f"{finder['class']} not implemented yet")
        return
    if to_find.match(args.URL, {}, f"/wp-content/plugins/{plugin}"):
        print(f'Version found for {plugin}: {to_find.matched}')
        return True
    return False

def detect_wordpress_plugins(args, finders):
    for i in finders:
        #print('-'*20)
        #print(i)
        #print('-'*20)
        for j in finders[i]:
            find_and_match(args, finders[i][j], i, j)
        #break