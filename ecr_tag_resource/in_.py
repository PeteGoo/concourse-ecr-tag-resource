#!/usr/bin/env python


import os, sys
import json

from .common import parse_input


def write_metadata_file(dest_dir: str, source: dict, attribute: str):
    with open(os.path.join(dest_dir, attribute), 'w') as metadata_file:
        metadata_file.write(source[attribute])


def in_(dest_dir, stdin):
    config = parse_input(stdin)
    image_id = config.get('version', {}).get('image-digest')

    if not image_id:
        raise Exception("Expected a version but got none")

    with open(os.path.join(dest_dir, 'timestamp'), 'w') as metadata_file:
        metadata_file.write(image_id)

    return {
        'version': {
            'image-digest': image_id
        },
        'metadata': []
    }


def main():
    versions = in_(sys.argv[1], sys.stdin)
    print(json.dumps(versions))
