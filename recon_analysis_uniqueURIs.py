import csv, json
from collections import Counter, defaultdict
from datetime import datetime, date, time


filetime = datetime.now()
filetime = filetime.strftime('%Y-%m-%d_%I-%M_%p')

#want to look in a column of URIs, figure out which ones appear more than once,
#and create a list of topic ids associated with those URIs

#making a bunch of lists
wikidata_URI_lists = []
wikidata_URI_pairs = []
wikidata_repeat_uris = []
counterlist = []

#opening the CSV that I exported from OpenRefine and put in Google sheets, to get rid of some extraneous columns
with open ('Reconciliation results analysis_March 2018.csv') as file:
	data = csv.reader(file)
	next(data, None)
	for row in data:
		#make a list of wikidata URIs
		wikidata_URI_list = []
		topicid = row[0]
		#lc_URI = row[2]
		#fast_URI = row[4]
		#viaf_URI = row[6]
		wikidata_URI = row[7]
		#put the wikidata uris in a list I'll pass to the collections Counter later
		counterlist.append(wikidata_URI)
		#add the URI and topic id to the list I made earlier in this for loop
		wikidata_URI_list.append(wikidata_URI)
		wikidata_URI_list.append(topicid)
		#add the list just populated with URI and topic id to another list
		wikidata_URI_lists.append(wikidata_URI_list)

#figure out which URIs are associated with more than one topic
count=Counter(counterlist)
for item in count:
	#if a URI is in more than one topic but less than 100, since the blanks ended up in there
	if count[item] > 1 and count[item] < 100:
		#add the URI to a list of wikidata URIs that appear more than once
		wikidata_repeat_uris.append(item)
#print(wikidata_repeat_uris)

d1 = defaultdict(list)

#create a dictionary with key of wikidata URI, value of list containing topic ids that URI has been matched to
#from this stack overflow: https://stackoverflow.com/questions/5378231/list-to-dictionary-conversion-with-multiple-values-per-key
for k, v in wikidata_URI_lists:
	if k in wikidata_repeat_uris:
		print(k)
		d1[k].append(v)

#print(d1.items())
d = dict((k, v) for k, v in d1.items())
print(d)
with open ('recon_analysis_repeatWikidataURIs_%s.json' %filetime, 'w') as f:
	json.dump(d, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it!")



