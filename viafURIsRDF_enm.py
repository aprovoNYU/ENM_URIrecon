import requests, json
#import xml.etree.ElementTree as ET
import rdflib
from rdflib import URIRef
from rdflib import Namespace
from rdflib.namespace import SKOS, RDFS, RDF

#from collections import Counter

#getting unique items in a list in a fast way, courtesy of https://www.peterbe.com/plog/uniqifiers-benchmark
#use this when extracting names
# def f5(seq, idfun=None): 
#    # order preserving
#    if idfun is None:
#        def idfun(x): return x
#    seen = {}
#    result = []
#    for item in seq:
#        marker = idfun(item)
#        # in old Python versions:
#        # if seen.has_key(marker)
#        # but in new ones:
#        if marker in seen: continue
#        seen[marker] = 1
#        result.append(item)
#    return result

#specify the schema.org namespace
schema=Namespace("http://schema.org/")
schema.name

#create a list for dictionaries containing the enrichment data
URIdictlist = []
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
			if "None" in VIAF_URL:
				pass
			
			else:
				#otherwise, the external link is the VIAF URI (the https one)
				URIdict["external_link"]["URL"] = VIAF_URI
				print(VIAF_URL)
				#to get the RDFXML, we use the http VIAF_URL and add the suffix
				VIAFRDFURL = str(VIAF_URL)+"/rdf.xml"
				#making an rdflib Graph
				g = rdflib.Graph()
				#try loading the RDFXML
				try:
					g.load(VIAFRDFURL)
					print(VIAFRDFURL)
				#if it doesn't work, print the bad VIAF URL (except I'm accidentally passing blank VIAF_URLs here, so it doesn't work)
				except:
					print("This VIAF URI had bad data:" + VIAF_URL)
					print(VIAFRDFURL)
					pass				# 	print(o)
				#create a list for shortened topic types, because there could be more than one
				shorttopictypelist = []
				#look in the graph for the objects in the triple where the subject is the VIAF URI and the predicate is rdf:type
				for a in g.objects(subject=rdflib.term.URIRef(VIAF_URL), predicate=RDF.type):
					topictype = a
					print(topictype)
					#We are interested in schema.org types
					if "schema" in topictype:
						#make it shorter, since we don't want the full URL in our data
						shorttopictype = topictype.replace("http://schema.org/", "schema:")
						print(shorttopictype)
					#sometimes theere's a productontology type though:
					elif "productontology" in topictype:
						shorttopictype = topictype.replace("http://www.productontology.org/id/", "pto:")
						print(shorttopictype)
					#add all the topic types to a list
					shorttopictypelist.append(shorttopictype)
					#print(shorttopictype)
					#put the list into the dictionary as the key-value for topic type
					URIdict["external_link"]["recon_data"]["topic_type"] = shorttopictypelist
					#would like to add a counter here to count how many topics will have at least one type added
				#not doing this, but this was how I got VIAF names before
# 				# viafnameslist = []

# 				# for x in g.objects(subject=None, predicate=SKOS.prefLabel):
# 				# 	viafpreflabel = x
# 				# 	#print(fastpreflabel)
# 				# 	viafnameslist.append(viafpreflabel.toPython())

# 				# for y in g.objects(subject=None, predicate=SKOS.altLabel):
					
# 				# 	viafaltlabel = y
# 				# 	#print(viafaltlabel)

# 				# 	viafnameslist.append(viafaltlabel.toPython())

# 				# for z in g.objects(subject=None, predicate=schema.name):

# 				# 	viafname = z
# 				# 	#print(viafname)
				
# 				# 	viafnameslist.append(viafname.toPython())
# 				# uniqueviafnameslist = f5(viafnameslist)
# 				# #print(uniqueviafnameslist)
# 				# URIdict["external_link"]["recon_data"]["topic_hits"] = uniqueviafnameslist

				#the URI dict is a record for each topic record to be enriched
				print(URIdict)
				URIdictlist.append(URIdict)
				#would like to add a counter here to report how many topics are being enriched. should match number of URIs found

# # name = g.value(None, SKOS.prefLabel, any=True)
# # print(name)
# # for s, p, o in g:
# # 	print(s)

#now we'll take the URIdict and make some JSON from it, and write it as a file.
with open ('VIAF_importantTopics_23March.json', 'w') as f:
	json.dump(URIdictlist, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")