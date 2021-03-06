import requests, json
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

#from https://www.pythoncentral.io/how-to-check-if-a-list-tuple-or-dictionary-is-empty-in-python/
def is_empty(any_structure):
    if any_structure:
        #print('Structure is not empty.')
        return False
    else:
        #print('Structure is empty.')
        return True

URIdictlist = []
alltopictypes = []
topictype_exceptions = []
#create variables for URI and blank URI field counts
countOfURIsAdded = 0
countOfnullURIs = 0
countOftopictypesAdded = 0


with open("schemaPerson_Wikidata_types.txt") as f:
    schemaPerson_list = f.read().splitlines()
    print(schemaPerson_list)

with open("schemaOrganization_Wikidata_types.txt") as f:
    schemaOrganization_list = f.read().splitlines()
    print(schemaOrganization_list)

with open("schemaCreativeWork_Wikidata_types.txt") as f:
    schemaCreativeWork_list = f.read().splitlines()
    print(schemaCreativeWork_list)

with open("schemaPlace_Wikidata_types.txt") as f:
    schemaPlace_list = f.read().splitlines()
    print(schemaPlace_list)

with open("schemaEvent_Wikidata_types.txt") as f:
    schemaEvent_list = f.read().splitlines()
    print(schemaEvent_list)

with open ("important_topics_to_enrich_2017_12_20_03_14_PM_cleaned-tsv_ORexport_2018_03_23_12-18pm.txt") as json_data:
	topics = json.load(json_data)
	for rows in topics:
		
		for topic in topics[rows]:
			URIdict = {}
			basketID = topic["Tct_Id"]
			Wikidata_URL = str(topic["Wikidata_URI"])
			#Wikidata_URL = Wikidata_URL.replace("/wiki", "/entity")
			#print(Wikidata_URL)
			URIdict["basket"] = basketID
			URIdict["external_link"] = {}
			if topic["Wikidata_closeMatch"] == "closeMatch":
				URIdict["external_link"]["link_type"] = "closeMatch"
			else:
				URIdict["external_link"]["link_type"] = "exactMatch"
			URIdict["external_link"]["label"] = "Wikidata"
			URIdict["external_link"]["recon_data"] = {}
			#print(URIdict)
			if "None" in Wikidata_URL or not Wikidata_URL:
				countOfnullURIs = countOfnullURIs + 1
				pass
			else:
				URIdict["external_link"]["URL"] = Wikidata_URL
				countOfURIsAdded = countOfURIsAdded + 1
				langlist = []
# # 				# Wikidata_testURL = "https://www.wikidata.org/wiki/Q7330150"
# # 				# WikidataID = Wikidata_testURL.replace("https://www.wikidata.org/wiki/","")
				WikidataID = Wikidata_URL.replace("https://www.wikidata.org/entity/","")
				#print(URIdictlist)
# 				#print(WikidataID)
				# r = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + WikidataID + "&format=json")
				# r.encoding = 'utf-8'
				# # "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q7330150&format=json"
				# Wikidatadata = json.loads(r.text)
				# #print(Wikidatadata["entities"][WikidataID]["labels"])
				# wikidatanameslist = []
				# names = Wikidatadata["entities"][WikidataID]["labels"]
				# #print(names)
				# for lang in names:
				# 	langlist.append(lang)
				# for item in langlist:
				# 	nameobject = Wikidatadata["entities"][WikidataID]["labels"][item]
				# 	actualname = nameobject["value"]
				# 	#print(actualname)
				# 	wikidatanameslist.append(actualname)

				# uniquewikidatanameslist = f5(wikidatanameslist)

				# URIdict["external_link"]["recon_data"]["topic_hits"] = uniquewikidatanameslist


				#Wikidata_testURL = "https://www.wikidata.org/wiki/Q7330150"
				#https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q7330150&format=json
				#WikidataID = Wikidata_testURL.replace("https://www.wikidata.org/wiki/","")
				r = requests.get("https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=" + WikidataID + "&format=json")
				r.encoding = "utf-8"
				Wikidataclaims = json.loads(r.text)
				try:
					topictypelist = []
					topictype = Wikidataclaims["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"]["id"]
					#print(topictype)

					r = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + topictype + "&format=json")
					r.encoding = "utf-8"
					Wikidatatopicname = json.loads(r.text)
					#print(Wikidatatopicname["entities"][topictype]["labels"])
					topictypename = Wikidatatopicname["entities"][topictype]["labels"]["en"]["value"]
					#print(topictypename)
					alltopictypes.append(topictypename)

					if topictypename in schemaPerson_list:
						topictypelist.append("schema:Person")
						countOftopictypesAdded = countOftopictypesAdded + 1
					elif topictypename in schemaOrganization_list:
						topictypelist.append("schema:Organization")
						countOftopictypesAdded = countOftopictypesAdded + 1
					elif topictypename in schemaEvent_list:
						topictypelist.append("schema:Event")
						countOftopictypesAdded = countOftopictypesAdded + 1
					elif topictypename in schemaPlace_list:
						topictypelist.append("schema:Place")
						countOftopictypesAdded = countOftopictypesAdded + 1
					elif topictypename in schemaCreativeWork_list:
						topictypelist.append("schema:CreativeWork")
						countOftopictypesAdded = countOftopictypesAdded + 1
					else:
						pass
#maybe could move this into the if statements?
					if is_empty(topictypelist) == False:
						URIdict["external_link"]["recon_data"]["topic_type"] = topictypelist
						print(URIdict)
				except:
					print("No P31")
					print(Wikidata_URL)
					topictype_exceptions.append(Wikidata_URL)
					#need to count how many
					pass
				


				# for lang in names:
				# 	if lang == "en":
				# 		for item in langlist:
				# 			nameobject = Wikidatadata["entities"][WikidataID]["labels"][item]
				# 			actualname = nameobject["value"]
					#print(actualname)

				print(URIdict)
				URIdictlist.append(URIdict)
				#need to count how many
uniquetopictypenames=f5(alltopictypes)
print(uniquetopictypenames)
print(topictype_exceptions)
print("blank URI field: ", countOfnullURIs, "| URIs added: ", countOfURIsAdded, "| topic types added: ", countOftopictypesAdded)

#in first pass, comment out code below in order to just print the unique topic names.
#Then use these to populate the text files that will generate the lists of Wikidata types to map to different schema.org properties
with open ("Wikidata_importantTopics_%s.json" %filetime, 'w') as f:
	json.dump(URIdictlist, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")


