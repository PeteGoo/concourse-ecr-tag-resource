import sys, json
import urllib.request


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_region():
    return json.loads(
        urllib.request.urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document').read().decode())[
        'region']


def parse_input(stdin=sys.stdin) -> (dict):
    input_doc = json.load(stdin)
    return input_doc
