#!/usr/bin/env python

import sys
import json

def check_(stdin) -> str:
    # We don't want any versions getting found by a check
    return []


def main():
    versions = check_(sys.stdin)
    print(json.dumps(versions))
