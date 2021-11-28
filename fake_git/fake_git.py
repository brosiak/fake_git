import os
import json
import hashlib


class States:
    NEW = "new"
    STAGED = "staged"
    MODIFIED = "modified"
    COMMITED = "commited"


REAL_GIT_NAME = ".git"
GIT_INIT_DIR_NAME = ".fake_git"
INIT_JSON_DICT = {
    States.NEW: {},
    States.STAGED: {},
    States.MODIFIED: {},
    States.COMMITED: {}
}
REPO_DIR = os.path.abspath(os.getcwd())
GIT_DIR = os.path.join(REPO_DIR, GIT_INIT_DIR_NAME)
GIT_JSON_NAME = "fake_git.json"
BLOCK_SIZE = 65536


def hash_file(file_name):
    os.chdir(REPO_DIR)
    file_hash = hashlib.sha256()
    with open(file_name, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def init_json():
    json_obj = json.dumps(INIT_JSON_DICT, indent=4)
    with open(GIT_JSON_NAME, "w") as outfile:
        outfile.write(json_obj)


def init_repository():
    os.mkdir(GIT_INIT_DIR_NAME)
    os.chdir(GIT_DIR)


def open_json(file_name):
    outfile = open(file_name, "r+")
    json_obj = json.load(outfile)
    return json_obj, outfile


def update_json(data, json_file):
    json_file.seek(0)
    json.dump(data, json_file, indent=4)
    json_file.truncate()
    json_file.close()


def fill_json_new_data():
    os.chdir(GIT_DIR)
    if not check_if_file_exists(GIT_JSON_NAME):
        return
    json_obj, json_file = open_json(GIT_JSON_NAME)
    dir_list = os.listdir(REPO_DIR)
    os.chdir(REPO_DIR)
    for file in dir_list:
        found = False
        if os.path.isdir(file):
            continue
        for command_files in json_obj.values():
            if file in command_files:
                found = True
                break
        if found:
            continue
        file_hash = hash_file(file)
        json_obj[States.NEW].update({file: file_hash})
    update_json(json_obj, json_file)


def check_if_file_exists(file_name):
    if file_name not in os.listdir(os.curdir):
        print("Error, no JSON FILE FOUND")
        return False
    return True


def update_modified_status():
    os.chdir(GIT_DIR)
    if not check_if_file_exists(GIT_JSON_NAME):
        return
    json_obj, json_file = open_json(GIT_JSON_NAME)
    dir_list = os.listdir(REPO_DIR)
    os.chdir(REPO_DIR)
    file_place = ''
    for file in dir_list:
        if os.path.isdir(file):
            continue
        file_hash = hash_file(file)
        if file in json_obj[States.NEW]:
            file_place = States.NEW
        elif file in json_obj[States.COMMITED]:
            file_place = States.COMMITED
        else:
            continue
        if file_hash == json_obj[file_place].get(file):
            continue
        del json_obj[file_place][file]
        json_obj[States.MODIFIED].update({file: file_hash})
    update_json(json_obj, json_file)


def display_file_statuses():
    os.chdir(GIT_DIR)
    if not check_if_file_exists(GIT_JSON_NAME):
        return
    json_obj, json_file = open_json(GIT_JSON_NAME)
    if States.COMMITED in json_obj:
        del json_obj[States.COMMITED]
    for state, files in json_obj.items():
        for file_name in files.keys():
            print(f"{file_name} ({state} file)")
    json_file.close()


def commit_files():
    os.chdir(GIT_DIR)
    if not check_if_file_exists(GIT_JSON_NAME):
        return
    json_obj, json_file = open_json(GIT_JSON_NAME)
    state = States.STAGED
    files = json_obj.get(state)
    files = {k: v for k, v in files.items()}
    for file_name, file_hash in files.items():
        del json_obj[state][file_name]
        json_obj[States.COMMITED].update({file_name: file_hash})
    update_json(json_obj, json_file)


def add_files(arg):
    os.chdir(GIT_DIR)
    if not check_if_file_exists(GIT_JSON_NAME):
        return
    json_obj, json_file = open_json(GIT_JSON_NAME)
    states = [States.NEW, States.MODIFIED]
    found = False
    for state in states:
        files = json_obj.get(state)
        files = {k: v for k, v in files.items()}
        if arg == "*":
            for file_name, file_hash in files.items():
                del json_obj[state][file_name]
                json_obj[States.STAGED].update({file_name: file_hash})
        elif arg in files:
            file_hash = files.get(arg)
            del json_obj[state][arg]
            json_obj[States.STAGED].update({arg: file_hash})
            found = True
    if not found and arg != "*":
        print(f"there is no file named {arg}")
        return
    update_json(json_obj, json_file)


def add(arg):
    fill_json_new_data()
    add_files(arg)


def status():
    fill_json_new_data()
    update_modified_status()
    display_file_statuses()


def init():
    if GIT_INIT_DIR_NAME in os.listdir(os.curdir):
        print("directory is already fake_git repository")
        return
    init_repository()
    init_json()
    fill_json_new_data()


def commit():
    commit_files()
