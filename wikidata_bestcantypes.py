import requests, json, csv
from datetime import datetime, date, time

filetime = datetime.now()
filetime = filetime.strftime('%Y-%m-%d_%I-%M_%p')

Recon_data_list =[]

with open ("wikidata_bestcantypes.txt") as tsv:
	for line in csv.reader(tsv, delimiter="\t"):
		WikidataID = line[0]
		reconcount = line[1]
	# for x in f.readlines():
	# 	x=x.strip()
	# 	WikidataID_list.append(x)
#print(Wikidata_id_list)
		WikidataID_name_recon =[]

	#print(WikidataID)
		r = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + WikidataID + "&format=json")
		r.encoding = 'utf-8'
		# "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q7330150&format=json"
		Wikidatadata = json.loads(r.text)
		try:
			WikidataID_name = Wikidatadata["entities"][WikidataID]["labels"]['en']['value']
			
			# print(WikidataID)
			# print(WikidataID_name)

		except:
			WikidataID_name = Wikidatadata["entities"][WikidataID]["labels"]['de']['value']

			# print(WikidataID)
			# print(WikidataID_name)

		WikidataID_name_recon.append(WikidataID)
		WikidataID_name_recon.append(WikidataID_name)
		WikidataID_name_recon.append(reconcount)
		print(WikidataID_name_recon)
		Recon_data_list.append(WikidataID_name_recon)

# for x in Recon_data_list:
# 	print(x)
# #print(Recon_data_list)
with open ("wikidata_bestcanmatches_%s.csv" %filetime, "w") as file:
	writer = csv.writer(file)
	writer.writerow(['WikidataID','WikidataName', 'ReconCount'])
	for y in Recon_data_list:
		row = y
		writer.writerow(row)
print("hooray we did it!")