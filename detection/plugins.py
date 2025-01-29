import httpx
import regex
from matchers.matcher_list import matcher_list, named_matcher_list, active_finders
import sys
from test_time import testtime
import asyncio
# TODO use finder name instead of class ?
# TODO modify it with a dict that map class directly to name
async def find_and_match(args, finder, plugin, name, content_dir):
    #print(f"{plugin}: {name}")
    if 'class' in finder and finder['class'] in matcher_list:
        to_find = matcher_list[finder['class']](name=plugin, **finder)
    elif name in named_matcher_list:
        to_find = named_matcher_list[name](name=plugin, **finder)
    else:
        #print(f"{name} not implemented yet")
        sys.exit(0)
        return False
    if await to_find.match(args.URL, path=f"{content_dir}/plugins/{plugin}"):
        #print(f'Version found for plugin {plugin} ({name} matcher): {to_find.version}')
        #sys.exit(0)
        return to_find.version
    return False

async def test_sync(args, finder, plugin, name, content_dir):
    #print(f"{plugin}: {name}")
    if 'class' in finder and finder['class'] in matcher_list:
        to_find = matcher_list[finder['class']](name=plugin, **finder)
    elif name in named_matcher_list:
        to_find = named_matcher_list[name](name=plugin, **finder)
    else:
        #print(f"{name} not implemented yet")
        sys.exit(0)
        return False
    if await to_find.match(args.URL, path=f"{content_dir}/plugins/{plugin}"):
        print(f'Version found for plugin {plugin} ({name} matcher): {to_find.version}')
        #sys.exit(0)
        return {"plugin": plugin, "name": name, "version": to_find.version}
    return False


def is_passive(finder, j):
    #if j in active_finders:
    #    return False
    #elif 'path' in finder[j]:
    if 'path' in finder[j]:
        return False
    return True

async def detect_wordpress_plugins(args, finders, content_dir):
    z = 0
    task = []
    print(content_dir)
    to_return = {}
    print(f"--- PLUGINS --- ")
    for i in finders:
        z += 1
        for j in finders[i]:
            passive = is_passive(finders[i], j)
            if args.mode == 'passive' and passive == False:
                continue
            elif args.mode == 'mixed' and passive == False and i not in args.popular_plugins:
                continue
            elif passive == False:
                #task.append(asyncio.ensure_future(test_sync(args, finders[i][j], i, j, content_dir)))
                continue
            print(z, i, j)
            tmp = testtime(f"{z} {i} {j}")
            detect = await find_and_match(args, finders[i][j], i, j, content_dir)
            tmp.end()
            if detect != False:
                if i not in to_return:
                    to_return[i] = []
                to_return[i].append({'method': j, 'version': detect})
        if i == "---------------info":
            sys.exit(0)
    print(len(task))
    #result_test = await asyncio.gather(*task)
    #for e in result_test:
    #    if e:
    #        print(e)
    #if args.mode == "passive":
    #    return to_return
    #print(to_return)
    #for i in to_return:
    #    version = None
    #    for j in to_return[i]:
    #        version = (j['version'] or version)
    #    if version == None:
    #        for j in finders[i]:
    #            print(j)
    #            detect = find_and_match(args, finders[i][j], i, j, content_dir)
    #            if detect != False:
    #                to_return[i].append({'method': j, 'version': detect})
#
    return to_return