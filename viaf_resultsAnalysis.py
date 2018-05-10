import requests, json
#import xml.etree.ElementTree as ET
import rdflib
from rdflib import URIRef
from rdflib import Namespace
from rdflib.namespace import SKOS, RDFS, RDF
from datetime import datetime, date, time
from collections import Counter

#create a list for dictionaries containing the enrichment data
URIdictlist = []
alltopictypes = []
countOfURIsAdded = 0
#open the export from OpenRefine
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
			VIAF_URI = topic["VIAF_URI"]
			#need to turn it into a string
			VIAF_URL = str(topic["VIAF_URI"])
			#for some reason, the RDFXML from VIAF uses http instead of https, so change that:
			VIAF_URL = VIAF_URL.replace("https", "http")
			#print(VIAF_URL)
			#create key-value pair for basket
			URIdict["basket"] = basketID
			#create a key for external link, whose value is a dictionary we'll fill in a moment
			URIdict["external_link"] = {}
			#create link type key in the external link dictionary, value is text "exactMatch"
			URIdict["external_link"]["link_type"] = "exactMatch"
			#since this is VIAF data, external link label is VIAF
			URIdict["external_link"]["label"] = "VIAF"
			#create a key for recon data, which is another dictionary that lives in the external link's dictionary
			URIdict["external_link"]["recon_data"] = {}

			#if there isn't a link, pass		
			if "None" in VIAF_URL or not VIAF_URL:
				pass
			
			else:
				#otherwise, the external link is the VIAF URI (the https one)
				URIdict["external_link"]["URL"] = VIAF_URI
				countOfURIsAdded = countOfURIsAdded + 1
				print(countOfURIsAdded)
print(countOfURIsAdded)

#also count types added
countoftypes = 0
typesadded =[]
typelistsadded = []
with open ("VIAF_importantTopics_2018-05-10_03-50_PM.json") as json_data:
	topics = json.load(json_data)
	for topic in topics:
		try: 
			topic_typelist=topic["external_link"]["recon_data"]["topic_type"]
			typelistsadded.append(topic_typelist)

			print(topic_typelist)

			for x in topic_typelist:
				typesadded.append(x)
		except:
			print("topic had no types")


print("Types added:")
for idx,item in enumerate(typesadded):
	print(idx+1, item)
print("Type lists added:")
for idx, item in enumerate(typelistsadded):
	print(idx+1, item)
	
# 			countoftypes = countoftypes +1
# 			print(countoftypes)
# print(countoftypes)

# listoftopicids = []

# with open ("VIAF_importantTopics_2018-04-04_04-11_PM.json") as json_results:
# 	topics = json.load(json_results)
# 	for topic in topics:
# 		print(topic)
# 		listoftopicids.append(topic["basket"])
# 		countOfURIsAdded = countOfURIsAdded+1
# 		print(countOfURIsAdded)
# print(countOfURIsAdded)
# count = Counter(listoftopicids)
# print(count)

