environment = './environment.yml'
not_installed = './error_message.txt'
desired_env = './new_environment.yml'

def remove_build(s: str) -> str:
    '''
    Removes the build from a string representing a package
    '''
    new_s = s[:s.rfind('=')]
    if '=' not in new_s: return s
    return new_s

def make_fuzzy(s: str) -> str:
    '''
    Changes the == to an = in the package specification
    '''
    return s.replace('==', '=', 1)

def make_exact(s: str) -> str:
    '''
    Does the opposite of above
    '''
    return s.replace('=', '==', 1)

if __name__ == '__main__':
    with open(not_installed) as n:
        not_installed_list = n.read().split('\n')
    with open(environment) as e:
        environment_list = e.read().split('\n')

    not_installed_list = [make_fuzzy(package) for package in not_installed_list]

    new_env_list = environment_list[:]
    matches = 0
    pip_location = 197
    assert 'pip:' in environment_list[pip_location]

    not_pip = set(environment_list[:pip_location])

    for package in not_installed_list:
        if package in not_pip:
            environment_list.remove(package)
            matches += 1
            environment_list.append('  ' + remove_build(make_exact(package)))
        else:
            print('The following package was not found in the environment.yml file:', package)

    with open(desired_env, 'w') as d:
        d.write('\n'.join(environment_list))

    if matches == len(not_installed_list):
        print(f'All {matches} packages were successfully moved under the \'pip\' section')
    else:
        print(f'There were {matches} packages out of {len(not_installed_list)} that were moved under the \'pip\' section.')
    
    input()