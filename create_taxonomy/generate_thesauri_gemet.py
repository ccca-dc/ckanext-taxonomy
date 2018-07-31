'''
convert GEMET rdf thesaurus to python dict.

download: https://www.eionet.europa.eu/gemet/rdf

'''

import rdflib
from rdflib.namespace import Namespace, RDF, RDFS
from glob import glob
from os.path import isfile
from pprint import PrettyPrinter
import json
import ckan.logic as logic
import ckan.model as model
from ckanapi import RemoteCKAN

# Wolfgang Start

graph = rdflib.Graph()

# convert to sane format :-)
if not isfile("gemet.n3"):
	for file in glob("gemet-*rdf"):
		graph.parse(file)
	with open("gemet.n3", "wb") as file:
		file.write(graph.serialize(format="n3"))


graph.load("gemet.n3", format="n3")

gns = dict(graph.namespaces())
SKOS = Namespace(gns["skos"])
GEMET = Namespace(gns["gemet"])

demo = RemoteCKAN('http://127.0.0.1:5000', apikey='')

tx = demo.call_action('taxonomy_create', {
		'title': 'GEMET',
		'name': 'GEMET',
		'uri': 'http://www.eionet.europa.eu/gemet',
		'last_modified': '2017-01-09'
		})

# tx = demo.call_action('taxonomy_show', {'name': 'gemet'})
print(tx)

# gemet sorted by supergroups and groups

r = graph.query('''
select ?uri ?label ?definition ?broader
where {
	<http://www.eionet.europa.eu/gemet/supergroup/> skos:member ?sg .
	?sg skos:member ?g .
	?g skos:member ?uri .
	?uri skos:prefLabel ?label .
	OPTIONAL { ?uri skos:definition ?definition . }
	OPTIONAL { ?uri skos:broader ?broader . }
}''', initNs={"rdf": RDF, "skos": SKOS})

concepts = list()

count = 0
for row in r:
	uri, label, definition, broader = tuple(x.toPython() if x is not None else '' for x in row)
	count = count + 1
	concept = dict()

	concept['uri'] = uri
	concept['broader'] = broader

	concepts.append(concept)
	print(uri)

	try:
		nd = demo.call_action('taxonomy_term_create', {
				'label': label,
				'uri': uri,
	 			'description': definition,
				'taxonomy_id': tx['id'],
				'parent_id': None
			})
	except:
		pass

print(count)


for c in concepts:
	if c['broader'] != '':
		print("update")
		print(c['uri'])
		broader_tax = demo.call_action('taxonomy_term_show', {
						'uri': c['broader']
					})

		broader_id = broader_tax.get('id')
		nd = demo.call_action('taxonomy_term_update', {
				'uri': c['uri'],
				'parent_id': broader_id
		})


# 	supergroup, group, concept = tuple(x.toPython() for x in row)
# 	if supergroup not in gemetgroups: gemetgroups[supergroup] = dict()
# 	if group not in gemetgroups[supergroup]: gemetgroups[supergroup][group] = list()
# 	gemetgroups[supergroup][group].append(concept)

# # sort concepts in each group
# for sg in gemetgroups:
# 	for g in gemetgroups[sg]:
# 		gemetgroups[sg][g].sort(key=unicode.lower)


# # sorted list of ALL concepts
# allconcepts = list()
# for sg in gemetgroups:
# 	for g in gemetgroups[sg]:
# 		allconcepts.extend(gemetgroups[sg][g])
# allconcepts.sort()


# gemet sorted by themes

# r=graph.query('''
# select distinct ?theme ?concept
# where {
# 	?th rdf:type gemet:Theme .
# 	?th rdfs:label ?theme .
# 	?th skos:member ?c .
# 	?c skos:prefLabel ?concept .
# }''', initNs={"rdf":RDF, "skos":SKOS, "gemet":GEMET})

# gemetthemes = dict()
# for row in r:
# 	theme, concept = tuple(x.toPython() for x in row)
# 	if theme not in gemetthemes: gemetthemes[theme] = []
# 	gemetthemes[theme].append(concept)



# # Wolfgang Ende

# demo = RemoteCKAN('http://127.0.0.1:5000', apikey='f5cb51ba-f15d-453f-b5d8-22f8baa03c8f')

# '''tx = demo.call_action('taxonomy_create', {
#         'title': 'gemet',
#         'name': 'gemet',
#         'uri': 'http://www.eionet.europa.eu/gemet'
#     })'''

# tx = demo.call_action('taxonomy_show', {
# 		'id': '8f7227c6-3c8e-4611-a9d9-69abafed1eda'
# 	})

# '''r = graph.query('''
# '''select *
# where {
# 	?p rdfs:label ?label .
# }
# '''''', initNs={"rdf": RDF, "skos": SKOS})

# for row in r:
# 	uri, label = tuple(x.toPython() for x in row)
# 	print("_____________________")
# 	print(label)
# 	print(uri)
# 	nd = demo.call_action('taxonomy_term_create', {
# 			'label': label,
# 	        'uri': uri,
# 	        'description': '',
# 	        'taxonomy_id': tx['id'],
# 	        'parent_id': None
# 	    })'''

# # creation of taxonomy terms without hierarchy
# '''r = graph.query('''
# '''select *
# where {
# 	?p skos:prefLabel ?prefLabel .
# }
# '''''', initNs={"rdf": RDF, "skos": SKOS})

# for row in r:
# 	uri, prefLabel = tuple(x.toPython() for x in row)
# 	print(uri)
# 	try:
# 		nd = demo.call_action('taxonomy_term_create', {
# 				'label': prefLabel,
# 		        'uri': uri,
# 		        'description': '',
# 		        'taxonomy_id': tx['id'],
# 		        'parent_id': None
# 		    })
# 	except:
# 		pass'''

# # updating terms with definition
# r = graph.query('''
# select *
# where {
# 	?p skos:definition ?definition .
# }
# ''', initNs={"rdf": RDF, "skos": SKOS})

# for row in r:
# 	uri, definition = tuple(x.toPython() for x in row)

# 	try:
# 		tax = demo.call_action('taxonomy_term_show', {
# 	            'uri': uri
# 	        })

# 		taxid = tax.get('id')

# 		nd = demo.call_action('taxonomy_term_update', {
# 				'id': taxid,
# 		        'uri': uri,
# 	            'description': definition
# 	        })
# 		print(uri)
# 	except:
# 		pass

# # updating of terms with parent_id
# '''r = graph.query('''
# '''select *
# where {
# 	?p skos:broader ?broader .
# }
# '''''', initNs={"rdf": RDF, "skos": SKOS})

# for row in r:
# 	uri, broader = tuple(x.toPython() for x in row)
# 	print(uri)

# 	try:
# 		broaderTax = demo.call_action('taxonomy_term_show', {
# 	            'uri': broader
# 	        })
# 		broaderid = broaderTax.get('id')
# 		currentTax = demo.call_action('taxonomy_term_show', {
# 	            'uri': uri
# 	        })

# 		currentid = currentTax.get('id')

# 		nd = demo.call_action('taxonomy_term_update', {
# 				'id': currentid,
# 		        'uri': uri,
# 	            'parent_id': broaderid
# 	        })
# 	except:
# 		pass'''

# # Wolfgang
# '''
# for g in gemetgroups:
# 	nd = demo.call_action('taxonomy_term_create', {
# 			'label': g,
#             'uri': '',
#             'description': g,
#             'taxonomy_id': tx['id'],
#             'parent_id': None
#         })

# # generate files

# with open("thesauri.py", "w") as output:
#     pp = PrettyPrinter(indent=4, stream=output)

#     output.write("GEMETGROUPS=")
#     pp.pprint(gemetgroups)

#     output.write("GEMETTHEMES=")
#     pp.pprint(gemetthemes)


# with open("gemetconcepts.json", "w") as output:
# 	json.dump(allconcepts, output)
