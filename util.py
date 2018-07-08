import yaml

from slugify import slugify as _slugify


def slugify(value):
    return _slugify(value, to_lower=True)


def get_publishers(fpath):
    with open(fpath) as f:
        publishers = yaml.load(f.read())

    for publisher in publishers:
        if 'slug' not in publisher:
            publisher['slug'] = slugify(publisher['name'])

    return publishers
