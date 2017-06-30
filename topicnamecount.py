import requests, json
import xml.etree.ElementTree as ET
import rdflib
from rdflib.namespace import SKOS, RDFS, RDF
from rdflib import Namespace
from collections import Counter

#http://stackoverflow.com/questions/1157106/remove-all-occurrences-of-a-value-from-a-python-list
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

alltopicslist = []

with open ("Topics_Z_allnames.txt") as json_data:
	topics = json.load(json_data)
	for rows in topics:
		
		for topic in topics[rows]:
			topicdisplay = topic["basket - display_name"]
			alltopicslist.append(topicdisplay)
			topicothername = topic["basket - topic_hits - __anonymous__ - name"]
			alltopicslist.append(topicothername)


with open ("WikidatatopicsZ_unique_30March.json") as wikijson_data:
	wikitopics = json.load(wikijson_data)
	for wikitopic in wikitopics:
		wikitopicnames = wikitopic["external_link"]["recon_data"]["topic_hits"]
		for wikitopicname in wikitopicnames:
			alltopicslist.append(wikitopicname)

with open ("LOCtopicsZ_unique_30March.json") as locjson_data:
	loctopics = json.load(locjson_data)
	for loctopic in loctopics:
		loctopicnames = loctopic["external_link"]["recon_data"]["topic_hits"]
		for loctopicname in loctopicnames:
			alltopicslist.append(loctopicname)

with open ("FASTtopicsZ_unique_30March.json") as fastjson_data:
	fasttopics = json.load(fastjson_data)
	for fasttopic in fasttopics:
		fasttopicnames = fasttopic["external_link"]["recon_data"]["topic_hits"]
		for fasttopicname in fasttopicnames:
			alltopicslist.append(fasttopicname)

with open ("VIAFtopicsZRDF_unique_30March.json") as viafjson_data:
	viaftopics = json.load(viafjson_data)
	for viaftopic in viaftopics:
		viaftopicnames = viaftopic["external_link"]["recon_data"]["topic_hits"]
		for viaftopicname in viaftopicnames:
			alltopicslist.append(viaftopicname)

cleanlist = remove_values_from_list(alltopicslist, None)
#print(cleanlist)
print(len(cleanlist))
uniquealltopicslist = set(cleanlist)
#print(uniquealltopicslist)
print(len(uniquealltopicslist))