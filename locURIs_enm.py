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
			LOC_URL = str(topic['LOC URL'])
			#print(VIAF_URL)
			URIdict["basket"] = basketID
			URIdict["external_link"] = {}
			URIdict["external_link"]["link_type"] = "exactMatch"
			URIdict["external_link"]["label"] = "Library of Congress"
			URIdict["external_link"]["recon_data"] = {}

# # # ###NEED to take the URI, grab JSON or XML; grab names and types, create JSON object with basket id, URL+linksource, topic type, and name(s)
		
			if "None" in LOC_URL:
				pass
			else:
				URIdict["external_link"]["URL"] = LOC_URL
				#print(LOC_URL)
				LOCntURL = str(LOC_URL +".skos.nt")

				g = rdflib.Graph()
				g.parse(LOCntURL, format="n3")
								# for s, p, o in g.triples((None, RDFS.label, None)):
								# 	#if "type" in p:
								# 	print(o)
				shorttopictypelist = []

				for a in g.objects(subject=rdflib.term.URIRef(LOC_URL), predicate=RDF.type):
					topictype = a
					shorttopictype = topictype.replace("http://www.w3.org/2004/02/skos/core#", "skos:")
					#print(shorttopictype)
					shorttopictypelist.append(shorttopictype)

					URIdict["external_link"]["recon_data"]["topic_type"] = shorttopictypelist


				locnameslist = []

				for x in g.objects(subject=None, predicate=SKOS.prefLabel):
					locpreflabel = x
					#print(locpreflabel)
					locnameslist.append(locpreflabel.toPython())

				for y in g.objects(subject=None, predicate=SKOS.altLabel):
					
					localtlabel = y
					#print(localtlabel)
					locnameslist.append(localtlabel.toPython())

				for z in g.objects(subject=None, predicate=schema.name):

					locname = x
					#print(locname)
					locnameslist.append(locname.toPython())

				uniquelocnameslist = f5(locnameslist)	
				URIdict["external_link"]["recon_data"]["topic_hits"] = uniquelocnameslist
				print(URIdict)
				URIdictlist.append(URIdict)


with open ('LOCtopicsZ_unique_30March.json', 'w') as f:
	json.dump(URIdictlist, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")