import re
from django.contrib import auth


def camel_case_to_underscore(name):
    """Convert camel cased SomeString to some_string"""

    return re.sub('([a-z0-9])([A-Z])', r'\1_\2',
                  re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)).lower()


def strip_suffixes(word, suffixes):
    """Strip suffixes from the word.

    Never strips whole word to empty string.
    """

    for suffix in suffixes:
        if word != suffix and word.endswith(suffix):
            word = word[:-len(suffix)]
    return word
