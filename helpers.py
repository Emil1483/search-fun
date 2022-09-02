import json
import logging
import os
import time
from datetime import datetime
from time import sleep


def flatten(t):
    return [item for sublist in t for item in sublist]

def path(file=None):
    return os.path.dirname(os.path.realpath(file or __file__))

def init_logging(file):
    build_logger_from(logging.getLogger(), file)

def build_logger(file):
    return build_logger_from(logging.getLogger(file), file)

def build_logger_from(logger: logging.Logger, file):
    for handler in logger.handlers:
        logger.removeHandler(handler)

    if len(logger.handlers) > 0: return logger

    logger.propagate = False

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    script_name, _ = os.path.splitext(os.path.basename(file))
    fh = logging.FileHandler(f'{path(file)}/logs/{script_name}.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

def log_about_file(file, log):
    formatted_time = datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')
    formatted_log = f'{formatted_time} {log}'

    print(f'Logging to {file}: {formatted_log}')

    script_name, _ = os.path.splitext(os.path.basename(file))
    with open(f'{path(file)}/logs/{script_name}.log', 'a') as f:
        f.write(f'\n{formatted_log}')

def assert_extension(filename, required_extension):
    _, extension = os.path.splitext(filename)
    assert extension == required_extension, f'file {filename} must end in {required_extension}'

def retry(function, attempts=10, fallback=None):
    error = None
    for _ in range(attempts):
        try:
            return function()
        except Exception as e:
            sleep(0.1)
            error = e

    if fallback: return fallback
    raise error

def read_txt(file, fallback=None):
    assert_extension(file, '.txt')

    if os.path.exists(f'{path()}/{file}'):
        with open(f'{path()}/{file}', 'r') as f:
            return f.read()

    with open(f'{path()}/{file}', 'w') as f:
        string = fallback or ''
        f.write(string)
        return string

def read_txt_as_bool(file, fallback=True):
    return retry(lambda: bool(int(read_txt(file))), fallback=fallback)

def write_txt_as_bool(file, b):
    write_txt(file, '1' if b else '0')

def read_html(file, fallback=None):
    assert_extension(file, '.html')

    if os.path.exists(f'{path()}/{file}'):
        with open(f'{path()}/{file}', 'r') as f:
            return f.read()

    with open(f'{path()}/{file}', 'w') as f:
        string = fallback or ''
        f.write(string)
        return string

def write_txt(file, text):
    assert_extension(file, '.txt')

    logging.debug(f'writing {text} to {file}' if len(text) < 20 else f'writing to {file}')

    with open(f'{path()}/{file}', 'w') as f:
        f.write(text)

read_json_cache = {}
def read_json(file, fallback=None, cache_timeout=None):
    assert_extension(file, '.json')

    if cache_timeout and file in read_json_cache:
        cache, timestamp = read_json_cache[file]
        age = time.time() - timestamp
        if age < cache_timeout: return cache

    if os.path.exists(f'{path()}/{file}'):
        def read():
            with open(f'{path()}/{file}', 'r') as s:
                result = json.load(s)
                read_json_cache[file] = result, time.time()
                return result
        return retry(read, fallback=fallback)

    with open(f'{path()}/{file}', 'w') as s:
        mdict = fallback if fallback is not None else {}
        json.dump(mdict, s, indent=4)
        return mdict

def write_json(file, mdict):
    assert_extension(file, '.json')

    logging.debug(f'writing {mdict} to {file}' if len(str(mdict)) < 20 else f'writing to {file}')

    with open(f'{path()}/{file}', 'w') as s:
        json.dump(mdict, s, indent=4)

def prettify(dictionary):
    return json.dumps(dictionary, indent=4)