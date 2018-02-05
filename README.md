# AWS ECR Tag Resource

[![Docker Build Status](https://img.shields.io/docker/build/petegoo/concourse-ecr-tag-resource.svg)](https://hub.docker.com/r/petegoo/concourse-ecr-tag-resource)

Allows Concourse to tag ECR repositories

- *check:* Does nothing
- *in:* Not useful right now
- *out:* Tag an ECR repository with the given tag

## Resource Type Configuration

```
resource_types:
- name: ecr-tag-resource
  type: docker-image
  source:
    repository: petegoo/concourse-ecr-tag-resource
    tag: latest
```

## Source Configuration
Make sure you have an ECR repository already setup.

- `repository`: _Optional._ The full Docker repository location of the ECR repository

```
resources:
- name: my-docker-image
  type: docker-image
  source:
    repository: 12345678.dkr.ecr.us-west-2.amazonaws.com/my-ecr-repository
```

## Behaviour

### `out`: Adds a tag to the matching image

You can just reference the output from a docker-image resource

```yaml
  - put: ecr-tag
    params:
      existing_digest: my-docker-image/digest
      new_tag: my-new-tag
```

#### Parameters

Optional:
- `existing_digest` _(Optional)_: The digest of an existing image. Can also be a relative path to a file containing the digest as returned from the docker-image resource
- `existing_tag` _(Optional)_: The tag of an existing image. Can also be a relative path to a file containing the tag as returned from the docker-image resource
- `repository` _(Optional)_: The full Docker repository location of the ECR repository. Can also be a relative path to a file containing the repository as returned from the docker-image resource
- `ignore_already_tagged` _(Optional)_: Whether to ignore the case when the image is already tagged as required. Default `true`

#### Examples

```yaml
jobs:

- name: tag-with-test
  plan:
  - get: my-image
  - put: ecr-tag
    params:
      existing_digest: my-image/digest
      new_tag: test

resources:
- name: ecr-tag
  type: ecr-tag-resource
  source:
    repository: 12345678.dkr.ecr.us-west-2.amazonaws.com/my-image

- name: my-image
  type: docker-image
  source:
    repository: 12345678.dkr.ecr.us-west-2.amazonaws.com/my-image

resource_types:

- name: ecr-tag-resource
  type: docker-image
  source:
    repository: petegoo/concourse-ecr-tag-resource
    tag: latest

```


