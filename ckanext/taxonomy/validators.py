
import ckan.lib.navl.dictization_functions as df
import ckan.logic as logic
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import json
import ast

from ckanext.scheming.validation import scheming_validator
ignore_empty = plugins.toolkit.get_validator('ignore_empty')


Invalid = df.Invalid
StopOnError = df.StopOnError
Missing = df.Missing
missing = df.missing

@scheming_validator
def taxonomy_check_vocab(field, schema):

    def validator(key, data, errors, context):

        # if there was an error before calling our validator
        # don't bother with our validation
        if errors[key]:
            return

        if data:
            tags = data.get(key)
        else:
            return

        if tags:
            tag_list = tags.split(',')
        else:
            return

        controlled_tags = data.get(('controlled_tags',))

        if controlled_tags:
            voc_list = json.loads(controlled_tags)
        else:
            return

        not_found =[]

        for x in tag_list:
            if any (d['taxonomy_term'] == x and d['taxonomy'] == "" for d in voc_list):
                not_found.append(x)

        if not_found:
            errors[key].append('Please use only keywords from controlled vocabularies: %s not found '  %', '.join(not_found))

    return validator

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
