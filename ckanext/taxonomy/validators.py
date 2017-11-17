
import ckan.lib.navl.dictization_functions as df
import ckan.logic as logic
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import json

from ckanext.scheming.validation import scheming_validator
ignore_empty = plugins.toolkit.get_validator('ignore_empty')


Invalid = df.Invalid
StopOnError = df.StopOnError
Missing = df.Missing
missing = df.missing

def taxonomy_check_vocab(key, data, errors, context):

# if there was an error before calling our validator
    # don't bother with our validation
    if errors[key]:
            return

    value = data.get(key)

    print key
    print value

    if value is not missing:
        if not isinstance(value, (list, str, unicode)):
            errors[key].append(_('expecting list of strings or dicts in list as string'))
            return
    else:
        return

def taxonomy_exists(value, context):
    try:
        logic.get_action('taxonomy_show')(context, {'uri': value})
    except logic.NotFound:
        raise Invalid('Taxonomy not found')
    except logic.ValidationError:
        raise Invalid('Taxonomy not found')
    return value


def taxonomy_exists_allow_empty(value, context):
    if not value:
        return value

    try:
        logic.get_action('taxonomy_show')(context, {'uri': value})
    except logic.NotFound:
        raise Invalid('Taxonomy not found')
    except logic.ValidationError:
        raise Invalid('Taxonomy not found')

    return value


def taxonomy_term_exists(value, context):
    try:
        logic.get_action('taxonomy_term_show')(context, {'uri': value})
    except logic.NotFound:
        raise Invalid('Term not found')
    except logic.ValidationError:
        raise Invalid('Term not found')
    return value
    pass


def taxonomy_term_exists_allow_empty(value, context):
    if not value:
        return value

    try:
        logic.get_action('taxonomy_term_show')(context, {'uri': value})
    except logic.NotFound:
        raise Invalid('Term not found')
    except logic.ValidationError:
        raise Invalid('Term not found')

    return value
