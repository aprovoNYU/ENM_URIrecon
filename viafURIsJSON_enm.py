import requests, json
from collections import Counter

URIdictlist = []

with open ("Topics_Z.txt") as json_data:
	topics = json.load(json_data)
	for rows in topics:
		
		for topic in topics[rows]:
			URIdict = {}
			basketID = topic['basket - id']
			LOC_URL = topic['LOC URL']
			VIAF_URL = topic['VIAF URL']
			FAST_URL = topic['FAST URL']

			URIdict["basket"] = basketID
			URIdict["external_link"] = {}
			URIdict["external_link"]["link_type"] = "exactMatch"
			URIdict["external_link"]["label"] = "VIAF"
			URIdict["external_link"]["recon_data"] = {}

# # ###NEED to take the URI, grab JSON or XML; grab names and types, create JSON object with basket id, URL+linksource, topic type, and name(s)
			if "None" in str(VIAF_URL):
				pass
			else:
				URIdict["external_link"]["URL"] = VIAF_URL
				# print(VIAF_URL)
				r = requests.get(VIAF_URL+"/viaf.jsonld")
				r.encoding = 'utf-8'

				# print(r.status_code)

				# print(r.text)

				# r = requests.get("http://viaf.org/viaf/76415840/viaf.jsonld")
				# r.encoding = 'utf-8'

				#print(r.status_code)

				VIAFdata = json.loads(r.text)

				#for graph in VIAFdata:
				try:
					alternateName = VIAFdata["@graph"][0]["alternateName"]
					URIdict["external_link"]["recon_data"]["topic_hits"] = alternateName
					print(alternateName)
					print(VIAF_URL)
					print("*****")

				except:
					print("no alt name, sorry")
					print(VIAF_URL)
					print("<<<<<<<<<")
					pass

				try:
					name = VIAFdata["@graph"][1]["alternateName"]
					print(name)
					print(">>>>>>>>>")

				except:
					print("not there, sorry brometheus")
					print(VIAF_URL)
					print("~~~~~~~")
					pass
				try:
					topictype = VIAFdata["@graph"][0]["@type"]
					URIdict["external_link"]["recon_data"]["topic_type"] = topictype
					#print(topictype)
				except:
					#print("no type here, bruh")
					pass
				# print(URIdict)
				URIdictlist.append(URIdict)
# print(URIdictlist)


with open ('VIAFtopicsZ.json', 'w') as f:
	json.dump(URIdictlist, f)
	print("HOORAY, you did it!")