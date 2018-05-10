import requests, json
#import xml.etree.ElementTree as ET
import rdflib
from rdflib import URIRef
from rdflib import Namespace
from rdflib.namespace import SKOS, RDFS, RDF
from datetime import datetime, date, time
from collections import Counter

# #create a list for dictionaries containing the enrichment data
# URIdictlist = []
# alltopictypes = []
# countOfURIsAdded = 0
# countOfnullURIs = 0

# with open ("important_topics_to_enrich_2017_12_20_03_14_PM_cleaned-tsv_ORexport_2018_03_23_12-18pm.txt") as json_data:
# 	topics = json.load(json_data)
# 	for rows in topics:
		
# 		for topic in topics[rows]:
# 			URIdict = {}
# 			basketID = topic["Tct_Id"]
# 			Wikidata_URI = topic["Wikidata_URI"]
# 			#print (basketID, "|", Wikidata_URI)
# 			Wikidata_URL = str(topic["Wikidata_URI"])
# 			#Wikidata_URL = Wikidata_URL.replace("/wiki", "/entity")
# 			URIdict["basket"] = basketID
# 			URIdict["external_link"] = {}
# 			if topic["Wikidata_closeMatch"] == "closeMatch":
# 				URIdict["external_link"]["link_type"] = "closeMatch"
# 			else:
# 				URIdict["external_link"]["link_type"] = "exactMatch"
# 			URIdict["external_link"]["label"] = "Wikidata"
# 			URIdict["external_link"]["recon_data"] = {}
# 			if "None" in Wikidata_URL or not Wikidata_URL:
# 				countOfnullURIs = countOfnullURIs + 1
# 				print("|", Wikidata_URL, countOfnullURIs, "|")
# 				pass
# 			else:
# 				URIdict["external_link"]["URL"] = Wikidata_URL
# 				countOfURIsAdded = countOfURIsAdded + 1
# 				print("|", Wikidata_URL, countOfURIsAdded, "|")
			
# print(countOfnullURIs, "|", countOfURIsAdded)


countoftypes = 0
typelistsadded = []
typesadded =[]
with open ("Wikidata_importantTopics_2018-05-09_02-08_PM.json") as json_data:
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