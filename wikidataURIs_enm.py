import requests, json
from collections import Counter
from datetime import datetime, date, time


filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")

#getting unique items in a list in a fast way, courtesy of https://www.peterbe.com/plog/uniqifiers-benchmark

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

URIdictlist = []


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
			if "None" in Wikidata_URL:
				pass
			else:
				URIdict["external_link"]["URL"] = Wikidata_URL
				URIdictlist.append(URIdict)
				langlist = []
# # 				# Wikidata_testURL = "https://www.wikidata.org/wiki/Q7330150"
# # 				# WikidataID = Wikidata_testURL.replace("https://www.wikidata.org/wiki/","")
				WikidataID = Wikidata_URL.replace("https://www.wikidata.org/entity/","")

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

				topictypelist = []
				#Wikidata_testURL = "https://www.wikidata.org/wiki/Q7330150"
				#https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q7330150&format=json
				#WikidataID = Wikidata_testURL.replace("https://www.wikidata.org/wiki/","")
				r = requests.get("https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=" + WikidataID + "&format=json")
				r.encoding = "utf-8"
				Wikidataclaims = json.loads(r.text)
				try:
					topictype = Wikidataclaims["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"]["id"]
					#print(topictype)

					r = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + topictype + "&format=json")
					r.encoding = "utf-8"
					Wikidatatopicname = json.loads(r.text)
					#print(Wikidatatopicname["entities"][topictype]["labels"])
					topictypename = Wikidatatopicname["entities"][topictype]["labels"]["en"]["value"]
					#print(topictypename)
					topictypelist.append(topictypename)
					URIdict["external_link"]["recon_data"]["topic_type"] = topictypelist
				except:
					print("No P31")
					print(Wikidata_URL)
					pass
				


				# for lang in names:
				# 	if lang == "en":
				# 		for item in langlist:
				# 			nameobject = Wikidatadata["entities"][WikidataID]["labels"][item]
				# 			actualname = nameobject["value"]
					#print(actualname)

				#print(URIdict)
				#URIdictlist.append(URIdict)
	
with open ("Wikidata_importantTopics_23March.json", 'w') as f:
	json.dump(URIdictlist, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")


