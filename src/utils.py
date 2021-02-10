import os
from pathlib import Path


def check_if_exists(name):
    json_file_path = get_file_path(name)
    check1 = Path(json_file_path).exists()
    js_file_path = json_file_path[:-2]
    check2 = Path(js_file_path).exists()
    check = check1 and check2
    return check


def get_file_path(name):
    filename = name + ".json"
    file_path = os.path.join("static/pipes", filename)
    return file_path


if __name__ == "__main__":
    _pipe_exists = check_if_exists("123")
