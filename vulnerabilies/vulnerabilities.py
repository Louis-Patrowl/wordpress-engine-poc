
from termcolor import colored
from packaging.specifiers import SpecifierSet
from packaging.version import Version

color_severity = {
    'Low': 'green',
    'Medium': 'yellow',
    'High': 'red',
    'Critical': 'light_red'
}

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

def query_vulnerabilities_by_plugin(collection, plugin_name):
    results = collection.find({"software.slug": plugin_name})
    return list(results)

def vulnerabilities_checker(plugins_detection, collection):
    for i in plugins_detection:
            print(colored(i, 'cyan'))
            version_found = None
            for j in plugins_detection[i]:
                print(f"Version {colored(j['version'], 'green')} detected by {colored(j['method'], 'light_blue')} ")
                if j['version'] != None:
                    if version_found == None:
                        version_found = j['version']
                    elif version_found != j['version']:
                        print(colored(f"ERROR {i}: VERSION FOUND ARE NOT THE SAME", 'red'))
            if version_found != None:
                to_check = Version(version_found)
                test_vuln = query_vulnerabilities_by_plugin(collection, i)
                for j in test_vuln:
                    #print(j["id"], j["title"])
                    version_range = get_version_range(j["software"][0]["affected_versions"])
                    if to_check in version_range:
                        print(colored(f"{j['cvss']['rating'].ljust(8)}: {j['title']}", color_severity[j['cvss']['rating']]), end=' ')
                        if 'PR:N' in j['cvss']['vector']:
                            print(colored('(UNAUTH)', 'cyan', attrs=['bold'])) 
                        else:
                            print('')