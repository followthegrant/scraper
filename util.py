import yaml

from slugify import slugify as _slugify


def slugify(value):
    return _slugify(value, to_lower=True)


def get_publisher(fpath):
    with open(fpath) as f:
        publisher = yaml.load(f.read())
    if 'slug' not in publisher:
        publisher['slug'] = slugify(publisher['name'])
    return publisher


def cleanup_breaks(value):
    return ' '.join(value.split()).strip()
