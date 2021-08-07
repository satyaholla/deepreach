environment = './environment.yml'
failures = './error_message.txt'
desired_env = './new_environment.yml'

if __name__ == '__main__':
    with open(failures) as f:
        old_failure_list =f.read().split('\n')
    with open(environment) as e:
        environment_list = e.read().split('\n')

    failure_list = [failure.replace('==', '=', 1) for failure in old_failure_list]

    new_env_list = environment_list[:]
    matches = 0
    pip_location = 197
    assert environment_list[pip_location] == '  - pip:'

    not_pip = set(environment_list[:pip_location])

    for failure in failure_list:
        if failure in not_pip:
            environment_list.remove(failure)
            matches += 1
            environment_list.append('  ' + failure.replace('=', '==', 1))
        else:
            print('HERE',failure)
    if matches == len(failure_list): print('YAY')

    with open(desired_env, 'w') as d:
        d.write('\n'.join(environment_list))

    print(matches)
    print(len(failure_list))
    input()

    for val in old_failure_list:
        new_val = val.replace('==', '=', 1)
        new_val = new_val.replace('=', '==', 1)
        if new_val != val:
            print(val)
            print(new_val)

    for val in old_failure_list:
        try: assert '==' in val
        except: print(val)
