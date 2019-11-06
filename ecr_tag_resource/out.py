#!/usr/bin/env python


import os, sys
import json
import boto3
from botocore.exceptions import ClientError

from .common import parse_input, get_region, eprint


def write_metadata_file(dest_dir: str, source: dict, attribute: str):
    with open(os.path.join(dest_dir, attribute), 'w') as metadata_file:
        metadata_file.write(source[attribute])


def validate_param(config: dict, name: str):
    if not config.get(name):
        raise Exception("Expected configuration param '{}' but it was missing.".format(name))


def validate_source_param(config: dict, name: str):
    if not config.get(name):
        raise Exception("Expected source parameter '{}' but it was missing.".format(name))


def get_contents_or_value(source_dir: str, value: str):
    if not value:
        return value

    try:
        file_candidate = os.path.join(source_dir, value)
        if os.path.exists(file_candidate):
            with open(file_candidate) as f:
                return f.read().strip()
    except Exception as e:
        eprint("Error opening file {}".format(e))
    return value


def out_(source_dir, stdin):
    config = parse_input(stdin)

    if not config.get('params'):
        config['params'] = {}

    params = config.get('params', {})
    source = config.get('source', {})

    existing_tag = params.get('existing_tag')
    existing_digest = params.get('existing_digest')
    new_tag = params.get('new_tag')

    ignore_already_tagged = params.get('ignore_already_tagged', 'True').lower() == 'true'

    repository = params.get('repository') or source.get('repository')

    if not repository:
        raise Exception("You must supply the repository parameter on either the source or the put params")

    if (not existing_tag) and (not existing_digest):
        raise Exception("You must supply either the existing_tag or existing_digest parameters")

    if not new_tag:
        raise Exception("You must supply the new_tag parameter")

    existing_tag = get_contents_or_value(source_dir, existing_tag)
    existing_digest = get_contents_or_value(source_dir, existing_digest)
    new_tag = get_contents_or_value(source_dir, new_tag)
    repository = get_contents_or_value(source_dir, repository)

    repository_name = repository.split('/',1)[-1]
    account_id = repository.split('.')[0]

    ecr = boto3.client('ecr', get_region())
    response = ecr.batch_get_image(
        registryId=account_id,
        repositoryName=repository_name,
        imageIds=[
            {'imageDigest': existing_digest} if existing_digest else {'imageTag': existing_tag}
        ]
    )

    # batch_get_image returns an image for each tag so we just need one

    if len(response['images']) == 0:
        eprint(json.dumps(response))
        raise Exception('Image searched returned no results')

    image_manifest = response['images'][0]['imageManifest']
    image_digest = response['images'][0]['imageId']['imageDigest']

    try:
        ecr.put_image(
            registryId=account_id,
            repositoryName=repository_name,
            imageManifest=image_manifest,
            imageTag=new_tag
        )
    except ClientError as e:
        eprint('Image is already tagged with {}'.format(new_tag))
        if e.response['Error']['Code'] == 'ImageAlreadyExistsException' and not ignore_already_tagged:
            raise e

    return {
        'version': {
            'image-digest': image_digest,
        }
    }


def main():
    versions = out_(sys.argv[1], sys.stdin)
    print(json.dumps(versions))
