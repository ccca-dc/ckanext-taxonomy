import ckan.model as model
import ckan.logic as logic
import json


def taxonomy(named_taxonomy):
    """ Returns the named taxonomy """
    ctx = {'model': model}
    return logic.get_action('taxonomy_show')\
        (ctx, {'name': named_taxonomy})


def taxonomy_terms(taxonomy_id):
    ctx = {'model': model}
    return logic.get_action('taxonomy_term_tree')\
        (ctx, {'id': taxonomy_id})


def get_taxonomies():
    ctx = {'model': model}
    taxonomy_list = logic.get_action('taxonomy_list')(ctx, {})
    return taxonomy_list


def parse_used_thesauri(used_thesauri):
    try:
        mdedit_used_thesauri = json.loads(used_thesauri)

        thesauri = []

        for t in mdedit_used_thesauri:
            thesaurus = t['taxonomy']
            if thesaurus != "" and thesaurus not in thesauri:
                thesauri.append(thesaurus.strip())

        return ', '.join(thesauri)
    except ValueError:
        return
