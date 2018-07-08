import yaml
from urllib.parse import urljoin

from slugify import slugify as _slugify


def slugify(value):
    return _slugify(value, to_lower=True)


def get_publishers(fpath):
    with open(fpath) as f:
        publishers = yaml.load(f.read())

    for publisher in publishers:
        publisher['slug'] = slugify(publisher['name'])

    return publishers


def get_absolute_url(base, url):
    if not url.startswith('http'):
        return urljoin(base, url)
    return url
