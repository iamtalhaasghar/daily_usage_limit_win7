import os, datetime, time
from crud import crud


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

def get_username():
    return os.path.basename(os.path.expanduser('~')).lower().replace(' ', '_')

def control_usage_db(history_key, max_usage):    
    rows = DB.SELECT('history', '*', where={'column': 'history_key', 'oper': '=', 'value': 'history_key'})
    if not rows:
        daily_usage = 0
        DB.INSERT_INTO('history', [history_key, daily_usage])
    else:
        daily_usage = int(rows[0][1])
    
    print(history_key, 'used for', daily_usage, 'secs or ', daily_usage // 60, 'mins today')
    wait = 10
    while daily_usage < max_usage:
        print('waiting for another', wait, 'secs')
        time.sleep(wait)
        daily_usage += wait
        DB.UPDATE('history', {'column': 'used', 'oper': '=', 'value': daily_usage}, {'column': 'history_key', 'oper': '=', 'value': history_key})
        print(history_key, 'used for', daily_usage, 'secs or ', daily_usage // 60, 'mins today')    
    shutdown_computer()

if __name__ == '__main__':
    #control_usage()
    
    # create database and necessary tables
    DB = crud('daily_usage.db')
    DB.CREATE_TABLE('history', 'history_key varchar(255), used int')
    DB.CREATE_TABLE('setting', 'name varchar(255), value varchar(255)')
    
    # set daily time limit
    rows = DB.SELECT('setting', '*', where={'column': 'name', 'oper': '=', 'value': 'daily_usage_in_sec'})
    if not rows:
        max_usage = 3900
        print('setting default daily usage to be ', max_usage//60, 'mins')
        DB.INSERT_INTO('setting', ['daily_usage_in_sec', '3900'])
    else:
        max_usage = int(rows[0][1])
    
    print('max_usage is:', max_usage, 'secs or ', max_usage // 60, 'mins today')
    username = get_username()
    history_key = '%s_%s' % (datetime.datetime.today().strftime('%Y_%m_%d'), username)
    print('history_key:', history_key)
    control_usage_db(history_key, max_usage)




