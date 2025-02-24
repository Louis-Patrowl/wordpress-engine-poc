import httpx
import regex
from matchers.matcher_list import matcher_list, named_matcher_list, active_finders
import sys
from test_time import testtime
import asyncio
from alive_progress import alive_bar
from time import sleep
from matchers.xpathMulti import xpathMatcherMulti
import json

async def find_and_match(args, finder, name, plugin, path=None):
    ### To change to avoid condition, better if based uniquely on named finder
    if 'class' in finder and finder['class'] in matcher_list:
        to_find = matcher_list[finder['class']](**finder)
    elif name in named_matcher_list:
        to_find = named_matcher_list[name](**finder)
    else:
        print(f"{name} not implemented yet")
        sys.exit(0)
    await to_find.match(args.URL, path=path)
    #if await to_find.match(args.URL, path=f"{content_dir}/plugins/{plugin}"):
    return plugin, to_find

def is_passive(finder, j):
    #if j in active_finders:
    #    return False
    #elif 'path' in finder[j]:
    if 'path' in finder[j]:
        return False
    return True

PLUGINS_DETECT_FINDERS = [
    xpathMatcherMulti(version=True,
        xpath='//link/@href|//script/@src',
        pattern=regex.compile(f'\/plugins\/([^\/]+)\/',regex.IGNORECASE)
    ),
]

async def detect_wordpress_plugins_link(args):
    to_return = []
    for finder in PLUGINS_DETECT_FINDERS:
        if await finder.match(args.URL):
            to_return += finder.version
        if await finder.match(args.URL, path='ThisPageDoesntExistPatrowl', status=[404]):
            to_return += finder.version
    return {x: {'finders':[], 'version_detected': False} for x in set(to_return)}
        
def rest_api_plugin(args):
    to_return = []
    plugins = {}
    response = httpx.get(args.URL + '/?rest_route=/')
    rest_route = json.loads(response.text)['routes']

    with open('./test_directory/scanned_plugins.json') as f:
        for i in f:
            tmp_json = json.loads(i)
            for j in tmp_json:
                if j in ['full-site-editing']:
                    break
                plugins[j] = tmp_json[j]

    for i in rest_route:
        for j in plugins:
            if i in plugins[j]:
                to_return.append(j)
                break
    return {x: {'finders':[], 'version_detected': False} for x in set(to_return)}

    

async def detect_wordpress_plugins(args, finders, content_dir):
    to_return = await detect_wordpress_plugins_link(args)
    print(to_return)
    to_return2 = rest_api_plugin(args)
    print(to_return2)
    to_return.update(to_return2)
    print(to_return)

    with alive_bar(len(finders),title='PLUGINS') as bar:   # default setting
        task = []
        for plugin in finders:
            bar()        
            for finder in finders[plugin]:
                passive = is_passive(finders[plugin], finder)
                if passive == False:
                    continue
                #    #task.append(asyncio.ensure_future(test_sync(args, finders[i][j], i, j, content_dir)))
                name, matcher = await find_and_match(args, finders[plugin][finder], finder, plugin)
                if matcher.detected:
                    if plugin not in to_return:
                        to_return[plugin] = {'finders':[], 'version_detected': False}
                    if matcher.version != None:
                        to_return[plugin]['version_detected']=True
                    to_return[plugin]['finders'].append({'method': finder, 'version': matcher.version})


    for plugin in to_return:
        if to_return[plugin]['version_detected'] == False and plugin in finders:
            for finder in finders[plugin]:
                task.append(asyncio.ensure_future(find_and_match(args, finders[plugin][finder], finder, plugin, None if is_passive(finders[plugin], finder) else f"{content_dir}/plugins/{plugin}")))
    print(len(task))
    result_test = await asyncio.gather(*task)
    for name, i in result_test:
        print(name, i.detected)
        if i.detected:
            to_return[name]['finders'].append({'method': f'', 'version': i.version})
            

    return to_return