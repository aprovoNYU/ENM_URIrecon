import requests, json
#import xml.etree.ElementTree as ET
import rdflib
from rdflib import Namespace
from rdflib.namespace import SKOS, RDFS, RDF
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
alltopictypes = []

with open ("important_topics_to_enrich_2017_12_20_03_14_PM_cleaned-tsv_ORexport_2018_03_23_12-18pm.txt") as json_data:
	topics = json.load(json_data)
	for rows in topics:
		#get to the topic records in the JSON
		for topic in topics[rows]:
			#create a dictionary to store key-value pairs that will be turned into JSON later
			URIdict = {}
			#map the basket ID to the terminology used in OpenRefine project
			basketID = topic["Tct_Id"]
			#here's the VIAF URI I found through OpenRefine
			# FAST_URI = topic["FAST_URI"]
			#need to turn it into a string
			FAST_URL = str(topic["FAST_URI"])
			#print(FAST_URL)
			#create key-value pair for basket
			URIdict["basket"] = basketID
			#create a key for external link, whose value is a dictionary we'll fill in a moment
			URIdict["external_link"] = {}
			#create link type key in the external link dictionary, value is text "exactMatch"
			if topic["Wikidata_closeMatch"] == "closeMatch":
				URIdict["external_link"]["link_type"] = "closeMatch"
			else:
				URIdict["external_link"]["link_type"] = "exactMatch"			
			#since this is VIAF data, external link label is FAST
			URIdict["external_link"]["label"] = "FAST"
			#create a key for recon data, which is another dictionary that lives in the external link's dictionary
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
				try:
					g.load(FASTRDFURL)
				except:
					print("This FAST URI didn't work:" + FAST_URL)
					print(FASTRDFURL)
					pass	
				shorttopictypelist = []
				for a in g.objects(subject=rdflib.term.URIRef(FAST_URL), predicate=RDF.type):
					topictype = a
					shorttopictype = topictype.replace("http://schema.org/", "schema:")
					print(shorttopictype)
					if shorttopictype != "schema:Intangible":
						shorttopictypelist.append(shorttopictype)

					alltopictypes.append(shorttopictype)

					URIdict["external_link"]["recon_data"]["topic_type"] = shorttopictypelist

				#not doing this, but this was how I got FAST names before

				# fastnameslist = []

				# for x in g.objects(subject=None, predicate=SKOS.prefLabel):
				# 	fastpreflabel = x
				# 	#print(fastpreflabel)
				# 	fastnameslist.append(fastpreflabel.toPython())
				# for y in g.objects(subject=None, predicate=SKOS.altLabel):
					
				# 	fastaltlabel = y
				# 	#print(fastaltlabel)
				# 	fastnameslist.append(fastaltlabel.toPython())

				# for z in g.objects(subject=None, predicate=schema.name):

				# 	fastname = x
				# 	#print(fastname)
				# 	fastnameslist.append(fastname.toPython())

				# uniquefastnameslist = f5(fastnameslist)
				# URIdict["external_link"]["recon_data"]["topic_hits"] = uniquefastnameslist


				print(URIdict)
				URIdictlist.append(URIdict)

# name = g.value(None, SKOS.prefLabel, any=True)
# print(name)
# for s, p, o in g:
# 	print(s)
uniquetopictypenames=f5(alltopictypes)
print(uniquetopictypenames)

with open ('FAST_importantTopics_26March.json', 'w') as f:
	json.dump(URIdictlist, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")