import requests, json
#import xml.etree.ElementTree as ET
import rdflib
from rdflib.namespace import SKOS, RDFS, RDF
from rdflib import Namespace
from collections import Counter
from datetime import datetime, date, time


filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")
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
#create variables for URI and blank URI field counts
countOfURIsAdded = 0
countOfnullURIs = 0

with open ("important_topics_to_enrich_2017_12_20_03_14_PM_cleaned-tsv_ORexport_2018_03_23_12-18pm.txt") as json_data:
	topics = json.load(json_data)
	for rows in topics:
		#get to the topic records in the JSON
		for topic in topics[rows]:
			#create a dictionary to store key-value pairs that will be turned into JSON later
			URIdict = {}
			#map the basket ID to the terminology used in OpenRefine project
			basketID = topic["Tct_Id"]
			#here's the LC URI I found through OpenRefine. Need to turn it into a string:
			LOC_URL = str(topic['LC_URI'])
			#print(VIAF_URL)
			#create key-value pair for basket
			URIdict["basket"] = basketID
			#create a key for external link, whose value is a dictionary we'll fill in a moment
			URIdict["external_link"] = {}
			#create link type key in the external link dictionary, value is text "exactMatch"
			if topic["LC_closeMatch"] == "closeMatch":
				URIdict["external_link"]["link_type"] = "closeMatch"
			else:
				URIdict["external_link"]["link_type"] = "exactMatch"
			#since this is Library of Congress data, external link label is Library of Congress
			URIdict["external_link"]["label"] = "Library of Congress"
			#create a key for recon data, which is another dictionary that lives in the external link's dictionary
			URIdict["external_link"]["recon_data"] = {}

# # # ###NEED to take the URI, grab JSON or XML; grab names and types, create JSON object with basket id, URL+linksource, topic type, and name(s)
			#for this round, decided not to grab any data from the LC URIs, so commenting this out.
			if "None" in LOC_URL or not LOC_URL:
				#add to count of blanks or nulls in the URI field
				countOfnullURIs = countOfnullURIs + 1
				pass
			else:
				URIdict["external_link"]["URL"] = LOC_URL
				#add to count of URIs added to data
				countOfURIsAdded = countOfURIsAdded + 1
				#print(LOC_URL)
			# 	LOCntURL = str(LOC_URL +".skos.nt")

			# 	g = rdflib.Graph()
			# 	try:
			# 		g.parse(LOCntURL, format="n3")
			# 					# for s, p, o in g.triples((None, RDFS.label, None)):
			# 					# 	#if "type" in p:
			# 	except:
			# 		print("This LC URI didn't work:", LOC_URL)
			# 						# 	print(o)
			# 	shorttopictypelist = []

			# 	for a in g.objects(subject=rdflib.term.URIRef(LOC_URL), predicate=RDF.type):
			# 		topictype = a
			# 		shorttopictype = topictype.replace("http://www.w3.org/2004/02/skos/core#", "skos:")
			# 		#print(shorttopictype)
			# 		shorttopictypelist.append(shorttopictype)
			# 		alltopictypes.append(shorttopictype)
					#URIdict["external_link"]["recon_data"]["topic_type"] = shorttopictypelist


				# locnameslist = []

				# for x in g.objects(subject=None, predicate=SKOS.prefLabel):
				# 	locpreflabel = x
				# 	#print(locpreflabel)
				# 	locnameslist.append(locpreflabel.toPython())

				# for y in g.objects(subject=None, predicate=SKOS.altLabel):
					
				# 	localtlabel = y
				# 	#print(localtlabel)
				# 	locnameslist.append(localtlabel.toPython())

				# for z in g.objects(subject=None, predicate=schema.name):

				# 	locname = x
				# 	#print(locname)
				# 	locnameslist.append(locname.toPython())

				# uniquelocnameslist = f5(locnameslist)	
				# URIdict["external_link"]["recon_data"]["topic_hits"] = uniquelocnameslist
				print(URIdict)
				URIdictlist.append(URIdict)
# uniquetopictypenames = f5(alltopictypes)
# print(uniquetopictypenames)
print("blanks: ", countOfnullURIs, "| URIs added: ", countOfURIsAdded)
with open ('LC_importantTopics_%s.json' %filetime, 'w') as f:
	json.dump(URIdictlist, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")