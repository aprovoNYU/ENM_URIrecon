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
			VIAF_URL = str(topic['VIAF URL'])
			#print(FAST_URL)
			URIdict["basket"] = basketID
			URIdict["external_link"] = {}
			URIdict["external_link"]["link_type"] = "exactMatch"
			URIdict["external_link"]["label"] = "VIAF"
			URIdict["external_link"]["recon_data"] = {}

# ###NEED to take the URI, grab JSON or XML; grab names and types, create JSON object with basket id, URL+linksource, topic type, and name(s)

			if "None" in VIAF_URL:
				pass
			else:
				URIdict["external_link"]["URL"] = VIAF_URL
# FAST_URL = "http://id.worldcat.org/fast/1533194"
# FASTRDFURL = "http://id.worldcat.org/fast/1533194/rdf.xml"
				VIAFRDFURL = str(VIAF_URL)+"/rdf.xml"
				g = rdflib.Graph()

				try:
					g.load(VIAFRDFURL)
								# for s, p, o in g.triples((None, RDFS.label, None)):
								# 	#if "type" in p:
				except:
					print("This VIAF URI had bad data")
					print(VIAF_URL)
					pass				# 	print(o)

				shorttopictypelist = []
				for a in g.objects(subject=rdflib.term.URIRef(VIAF_URL), predicate=RDF.type):
					topictype = a
					if "schema" in topictype:
						shorttopictype = topictype.replace("http://schema.org/", "schema:")
					elif "productontology" in topictype:
						shorttopictype = topictype.replace("http://www.productontology.org/id/", "pto:")
					
					shorttopictypelist.append(shorttopictype)
					#print(shorttopictype)
					URIdict["external_link"]["recon_data"]["topic_type"] = shorttopictypelist


				viafnameslist = []

				for x in g.objects(subject=None, predicate=SKOS.prefLabel):
					viafpreflabel = x
					#print(fastpreflabel)
					viafnameslist.append(viafpreflabel.toPython())

				for y in g.objects(subject=None, predicate=SKOS.altLabel):
					
					viafaltlabel = y
					#print(viafaltlabel)

					viafnameslist.append(viafaltlabel.toPython())

				for z in g.objects(subject=None, predicate=schema.name):

					viafname = z
					#print(viafname)
				
					viafnameslist.append(viafname.toPython())
				uniqueviafnameslist = f5(viafnameslist)
				#print(uniqueviafnameslist)
				URIdict["external_link"]["recon_data"]["topic_hits"] = uniqueviafnameslist
				#print(URIdict)
				URIdictlist.append(URIdict)

# name = g.value(None, SKOS.prefLabel, any=True)
# print(name)
# for s, p, o in g:
# 	print(s)


with open ('VIAFtopicsZRDF_unique_30March.json', 'w') as f:
	json.dump(URIdictlist, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")