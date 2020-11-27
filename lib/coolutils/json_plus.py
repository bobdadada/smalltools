import json
import os
import six
import hashlib

from .extern import minify_json

def write_json(path, data):

    path = os.path.abspath(path)

    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(path, 'w', encoding='utf-8') as fd:
        json.dump(data, fd, indent=4, sort_keys=True)

def load_json(path, js_comments=False):

    path = os.path.abspath(path)

    with open(path, 'r', encoding='utf-8') as fd:
        content = fd.read()

    if js_comments:
        content = minify_json.json_minify(content)
        content = content.replace(",]", "]")
        content = content.replace(",}", "}")

    try:
        d = json.loads(content)
    except ValueError as e:
        raise Exception(
            "Error parsing JSON in file '{0}': {1}".format(
                path, six.text_type(e)))

    return d


