DEEPREACH_DIR = '/'.join(__file__.split('/')[:-2])

environment = f'{DEEPREACH_DIR}/environment.yml'
not_installed = f'{DEEPREACH_DIR}/change_env_file/packages_not_found.txt'
not_in_osx = f'{DEEPREACH_DIR}/change_env_file/not_in_osx.txt'
desired_env = f'{DEEPREACH_DIR}/new_environment.yml'

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
    with open(not_installed) as ni:
        not_installed_list = ni.read().split('\n')
    with open(not_in_osx) as nio:
        not_in_osx_list = nio.read().split('\n')
    with open(environment) as e:
        env_list = e.read().split('\n')

    not_installed_list = [make_fuzzy(package) for package in not_installed_list]
    new_env_list = env_list[:]
    matches = 0
    indices = {val: index for index, val in enumerate(env_list)}

    for package in not_installed_list:
        index = indices.get(package, -1)
        if index != -1:
            new_env_list[index] = remove_build(new_env_list[index])
            matches += 1
        else:
            print('The following package was not found in the environment.yml file:', package)
    
    if matches == len(not_installed_list):
        print(f'All {matches} packages had their build strings removed!')
    else:
        print(f'There were {matches} packages out of {len(not_installed_list)} whose build string was removed.')

    matches = 0
    for package in not_in_osx_list:
        for e_package in new_env_list:
            if package in e_package:
                new_env_list.remove(e_package)
                new_env_list.append('  ' + make_exact(package))
                matches += 1
                break
        else:
            print('The following package was not found in the environment.yml file:', package)
    
    if matches == len(not_in_osx_list):
        print(f'All {matches} packages were moved under the pip section!')
    else:
        print(f'There were {matches} packages out of {len(not_in_osx_list)} which were moved under the pip section.')

    with open(desired_env, 'w') as d:
        d.write('\n'.join(new_env_list))
    # with open(not_installed) as n:
    #     not_installed_list = n.read().split('\n')
    # with open(environment) as e:
    #     environment_list = e.read().split('\n')

    # not_installed_list = [make_fuzzy(package) for package in not_installed_list]

    # new_env_list = environment_list[:]
    # matches = 0
    # pip_location = 197
    # assert 'pip:' in environment_list[pip_location]

    # not_pip = set(environment_list[:pip_location])

    # for package in not_installed_list:
    #     if package in not_pip:
    #         new_env_list.remove(package)
    #         matches += 1
    #         new_env_list.append('  ' + remove_build(make_exact(package)))
    #     else:
    #         print('The following package was not found in the environment.yml file:', package)

    # with open(desired_env, 'w') as d:
    #     d.write('\n'.join(new_env_list))

    # if matches == len(not_installed_list):
    #     print(f'All {matches} packages were successfully moved under the \'pip\' section')
    # else:
    #     print(f'There were {matches} packages out of {len(not_installed_list)} that were moved under the \'pip\' section.')
    
    # input()