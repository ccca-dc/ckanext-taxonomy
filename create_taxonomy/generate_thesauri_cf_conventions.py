from rdflib.namespace import Namespace, RDF, RDFS
from glob import glob
from os.path import isfile
from pprint import PrettyPrinter
import ckan.logic as logic
import ckan.model as model
from ckanapi import RemoteCKAN
import xml.etree.ElementTree as ET

#tree = ET.parse('area-type-table.xml')
tree = ET.parse('cf-standard-name-table.xml')
root = tree.getroot()

demo = RemoteCKAN('http://127.0.0.1:5000', apikey='')

title = "CF conventions"

for title in root.iter('title'):
    title = title.text

# tx = demo.call_action('taxonomy_show', {
#         'uri': 'http://cfconventions.org'})


tx = demo.call_action('taxonomy_create', {
       'title': 'CF Standard Names',
       'name': 'CF Standard Names',
       'last_modified': '2017-03-28',
       'uri': 'http://cfconventions.org'
   })

for entry in root.findall('entry'):
    label = entry.get('id')
    description = entry[0].text
    # print(description)

    try:
        nd = demo.call_action('taxonomy_term_create', {
                'label': label,
                'uri': None,
                'description': description,
                'taxonomy_id': tx['id'],
                'parent_id': None
            })
        print(label)
    except:
        pass
