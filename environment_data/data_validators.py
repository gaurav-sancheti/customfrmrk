import re
from uuid import UUID


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except (ValueError, TypeError) as e:
        print(e)
        return False

    return True


def validate_url(url):
    url_regex = re.compile(
        r'^(http|https)://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(url_regex, url) is not None:
        return True
    else:
        return False
