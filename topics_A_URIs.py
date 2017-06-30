import requests, json
from collections import Counter
LOC_URIs=[]
URIdict = {}
with open ("topics_A_selection-json (3).txt") as json_data:
	topics = json.load(json_data)
	for rows in topics:
		for topic in topics[rows]:
			for element in topic:
				if element == "_ - id":
					basketID = topic[element]
				if element == "LOC ID" and topic[element] != None:
					# if topic[element] != None:	
					LOC_URL = topic[element]
					LOC_uribasket = basketID, LOC_URL
					LOC_URIs.append(LOC_uribasket)

				elif element == "VIAF ID" and topic[element] != None:
					VIAF_ID = topic[element]
					VIAF_URL = "http://viaf.org/viaf/" + VIAF_ID
					#print(VIAF_URL)
				elif element == "FAST URL" and topic[element] != None:
					FAST_URL = topic[element]
#print(LOC_URIs)
for tupl in LOC_URIs:
	# print(tupl[1])
# d=dict(LOC_URIs)
# print(d)

###NEED to take the URI, grab JSON or XML; grab names and types, create JSON object with basket id, URL+linksource, topic type, and name(s)
	r = requests.get(tupl[1]+".json")
	r.encoding = 'utf-8'

	# print(r.status_code)

	# print(r.text)

# # #turn it into a python dictonary

	LCdata = json.loads(r.text)
# #
# #to know how many things are in this variable: print(len(data))
# #print(data)
# #i = 0  this is to make a "counter"
	for record in LCdata:
		for x in record:
			if x == "http://www.loc.gov/mads/rdf/v1#authoritativeLabel":
				print(record[x])
	# for key in record:
	# 	if key == 'id':
	# 		documentID = str(record[key])
	# 	if key == 'publisher':
	# 		publisher = str(record[key])
	# 		#print(publisher)
	# 		if "Michigan" in publisher:
	# 			#print(publisher)
	# 			documentlist.append(documentID)

# #print(documentlist)


# uniquedocumentlist = set(documentlist)
# #print(uniquedocumentlist)

# # print(Counter(documentlist))
# # print(Counter(uniquedocumentlist))

# for item in uniquedocumentlist:

# 	r2 = requests.get('https://nyuapi.infoloom.nyc/api/hit/basket/search/?document='+ documentID)
# 	r2.encoding = 'utf-8'	
# 	#print(r2.status_code)
# 	#print(r2.text)
# 	#character encoding is getting weird here
# 	topic_minimal = json.loads(r2.text)
# 	#when printing, the characters display weird
# 	#print(topic_minimal)
# 	topic_list.append(topic_minimal)

# # uniquetopiclist = set(topic_list)
# # print(uniquetopiclist)
# # with open ('michigantopics_minimal.json', 'w') as f:
# # 	json.dump(topic_list, f)
# # 	print("HOORAY, you did it!")

# #now a dictionary in a list
# for item in topic_list:
# 	#print(item)
# 	for dictionary in item:
# 		for key in dictionary:
# 	 		if key == 'id':
# 	 			basketID = str(dictionary[key])
# 	 			#print(basketID)
# 	 			basketlist.append(basketID)

# #print(basketlist)

# uniquebasketlist = set(basketlist)
# #print(uniquebasketlist)

# # print(Counter(basketlist))
# # print(Counter(uniquebasketlist))
# print(len(uniquebasketlist))

# for thing in uniquebasketlist:

# 	r3 = requests.get('https://nyuapi.infoloom.nyc/api/hit/basket/'+ thing)
# 	r3.encoding = 'utf-8'	
# 	print(r3.status_code)
# 	print(r3.text)
# 	topic_record = json.loads(r3.text)
# 	print(topic_record)
# 	topic_records.append(topic_record)


# with open ('michigantopics_full.json', 'w') as f:
# 	json.dump(topic_records, f)
# 	print("HOORAY, you did it!")