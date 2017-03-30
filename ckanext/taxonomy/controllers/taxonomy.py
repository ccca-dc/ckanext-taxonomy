import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

from urllib import urlencode

from ckan.common import config
from paste.deploy.converters import asbool
import paste.fileapp

import ckan.lib.maintain as maintain
import ckan.lib.i18n as i18n
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.helpers as h
import ckan.lib.datapreview as datapreview
import ckan.lib.plugins
import ckan.lib.uploader as uploader
import ckan.lib.render
import json

from ckan.common import OrderedDict, _, json, request, c, g, response

get_action = logic.get_action


class TaxonomyController(base.BaseController):

    def index(self):
        context = {
            'model': model,
            'user': toolkit.c.user
        }

        toolkit.c.taxonomies = logic.get_action('taxonomy_list')(context, {})

        return toolkit.render('ckanext/taxonomy/index.html')

    def show(self, name):
        context = {
            'model': model,
            'user': toolkit.c.user
        }

        toolkit.c.taxonomy = logic.get_action('taxonomy_show')(
            context,
            {'id': name})

        toolkit.c.terms = logic.get_action('taxonomy_term_tree')(
            context,
            {'id': toolkit.c.taxonomy['id']})

        return toolkit.render('ckanext/taxonomy/show.html')

    def get_infos_from_keyword_label(self):
        label = request.POST.get('label')
        thesaurus = request.POST.get('thesaurus')

        context = {'model': model, 'session': model.Session,
                   'user': c.user}

        context = {'user': c.user}

        if thesaurus == "":
            try:
                term = get_action('taxonomy_term_show_all')(context, {'label': label})
            except logic.NotFound:
                return json.dumps([""])

            taxonomy_term = term[0]

            for t in term:
                if "gemet" in t['uri']:
                    taxonomy_term = t

            taxonomy_id = taxonomy_term['taxonomy_id']
            taxonomy = get_action('taxonomy_show')(context, {'id': taxonomy_id})
        else:
            taxonomy = get_action('taxonomy_show')(context, {'name': thesaurus})
            try:
                taxonomy_term = get_action('taxonomy_term_show')(context, {'label': label, 'taxonomy_id': taxonomy['id']})
            except logic.NotFound:
                return json.dumps([""])

        result = [taxonomy['name']]
        result.append(taxonomy_term['uri'])
        result.append(taxonomy['last_modified'])

        return json.dumps(result)
