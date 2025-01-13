import httpx
import regex
from matchers.matcher_list import matcher_list, named_matcher_list
import sys
from test_time import testtime

# TODO use finder name instead of class ?
# TODO modify it with a dict that map class directly to name
def find_and_match(args, finder, plugin, name, cached_request):
    #print(f"{plugin}: {name}")
    if 'class' in finder and finder['class'] in matcher_list:
        to_find = matcher_list[finder['class']](**finder)
    elif name in named_matcher_list:
        to_find = named_matcher_list[name](**finder)
    else:
        print(f"{finder['class']} not implemented yet")
        return
    if to_find.match(args.URL, {}, f"wp-content/plugins/{plugin}"):
        print(f'Version found for {plugin} with {name}: {to_find.matched}')
        #sys.exit(0)
        return True
    return False


def detect_wordpress_plugins(args, finders, cached_request):
    z = 0
    print(len(args.popular_plugins))
    for i in args.popular_plugins:
        z += 1
        if i not in finders:
            continue
        for j in finders[i]:
            if (j == 'Readme'):
                continue
            #print(z, i, j)
            tmp = testtime(f"{z} {i} {j}")
            find_and_match(args, finders[i][j], i, j, cached_request)
            tmp.end()
        #break