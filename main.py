# get current date only
def get_current_datetime_as_str():
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# get current date only
def get_current_date_as_str():
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d')

# get user home directory
def get_user_home_dir():
    import os
    dir_path = os.path.join(os.path.expanduser('~'), 'daily_usage')
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


# start script in background
def start_script_in_background(script_path):
    import subprocess
    subprocess.Popen(script_path, shell=True)
    return

# shutdown computer
def shutdown_computer():
    import os
    #os.system('shutdown -s -t 0')
    os.system('shutdown -l -f')
    return

# create a file in the user home directory
def create_file_in_user_home_dir(file_name):
    import os
    path = os.path.join(get_user_home_dir(), file_name)
    # check if file exists
    if os.path.isfile(path):
        print('File already exists: ' + path)
    else:
        open(path, 'w').close()
        print(path)
    return path


# write session info to file
def write_session_info_to_file(path, session_info):
    # write session info to file
    with open(path, 'a') as f:
        f.write(session_info + '\n')
    return

def count_all_sessions(path):
    import re
    return sum([int(i) for i in re.findall('>(.*)', open(path, 'r').read())])

def control_usage():
    import time
    file_path = create_file_in_user_home_dir(get_current_date_as_str() + '.txt')
    daily_usage = count_all_sessions(file_path)
    max_usage = 3900 # max daily usage in secs
    wait = 10
    while daily_usage < max_usage:
        print('waiting for another', wait, 'secs')
        time.sleep(wait)
        write_session_info_to_file(file_path, get_current_datetime_as_str() + '>' + str(wait))
        daily_usage = count_all_sessions(file_path)
    shutdown_computer()

if __name__ == '__main__':
    control_usage()



