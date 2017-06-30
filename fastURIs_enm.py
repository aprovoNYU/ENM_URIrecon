import requests, json
import xml.etree.ElementTree as ET
import rdflib
from rdflib.namespace import SKOS, RDFS, RDF
from rdflib import Namespace
from collections import Counter

#getting unique items in a list in a fast way, courtesy of https://www.peterbe.com/plog/uniqifiers-benchmark

def f5(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


schema=Namespace("http://schema.org/")
schema.name

URIdictlist = []
with open ("Topics_Z.txt") as json_data:
	topics = json.load(json_data)
	for rows in topics:
		
		for topic in topics[rows]:
			URIdict = {}
			basketID = topic['basket - id']
			FAST_URL = str(topic['FAST URL'])
			#print(FAST_URL)
			URIdict["basket"] = basketID
			URIdict["external_link"] = {}
			URIdict["external_link"]["link_type"] = "exactMatch"
			URIdict["external_link"]["label"] = "FAST"
			URIdict["external_link"]["recon_data"] = {}

# ###NEED to take the URI, grab JSON or XML; grab names and types, create JSON object with basket id, URL+linksource, topic type, and name(s)

			if "None" in FAST_URL:
				pass
			else:
				URIdict["external_link"]["URL"] = FAST_URL
# FAST_URL = "http://id.worldcat.org/fast/1533194"
# FASTRDFURL = "http://id.worldcat.org/fast/1533194/rdf.xml"
				FASTRDFURL = str(FAST_URL)+"/rdf.xml"
				g = rdflib.Graph()
			
				g.load(FASTRDFURL)
								# for s, p, o in g.triples((None, RDFS.label, None)):
								# 	#if "type" in p:
								# 	print(o)
				shorttopictypelist = []
				for a in g.objects(subject=rdflib.term.URIRef(FAST_URL), predicate=RDF.type):
					topictype = a
					shorttopictype = topictype.replace("http://schema.org/", "schema:")
					print(shorttopictype)
					shorttopictypelist.append(shorttopictype)
					URIdict["external_link"]["recon_data"]["topic_type"] = shorttopictypelist


				fastnameslist = []

				for x in g.objects(subject=None, predicate=SKOS.prefLabel):
					fastpreflabel = x
					#print(fastpreflabel)
					fastnameslist.append(fastpreflabel.toPython())
				for y in g.objects(subject=None, predicate=SKOS.altLabel):
					
					fastaltlabel = y
					#print(fastaltlabel)
					fastnameslist.append(fastaltlabel.toPython())

				for z in g.objects(subject=None, predicate=schema.name):

					fastname = x
					#print(fastname)
					fastnameslist.append(fastname.toPython())

				uniquefastnameslist = f5(fastnameslist)
				URIdict["external_link"]["recon_data"]["topic_hits"] = uniquefastnameslist
				print(URIdict)
				URIdictlist.append(URIdict)

# name = g.value(None, SKOS.prefLabel, any=True)
# print(name)
# for s, p, o in g:
# 	print(s)


with open ('FASTtopicsZ_unique_30March.json', 'w') as f:
	json.dump(URIdictlist, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")