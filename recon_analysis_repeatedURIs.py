import csv, json
from collections import Counter, defaultdict
from datetime import datetime, date, time


def count_uris(counterlist, repeaturis_list):
	count=Counter(counterlist)
	for item in count:
		#if a URI is in more than one topic but less than 100, since the blanks ended up in there
		if count[item] > 1 and count[item] < 100:
			#add the URI to a list of wikidata URIs that appear more than once
			repeaturis_list.append(item)
	return repeaturis_list

def result_dictionary(URI_lists, repeaturis_list):

	d1 = defaultdict(list)

	#create a dictionary with key of URI, value of list containing topic ids that URI has been matched to
	#from this stack overflow: https://stackoverflow.com/questions/5378231/list-to-dictionary-conversion-with-multiple-values-per-key
	for k, v in URI_lists:
		if k in repeaturis_list:
			print(k)
			d1[k].append(v)

	#print(d1.items())
	d = dict((k, v) for k, v in d1.items())
	return d

filetime = datetime.now()
filetime = filetime.strftime('%Y-%m-%d_%I-%M_%p')

#want to look in a column of URIs, figure out which ones appear more than once,
#and create a list of topic ids associated with those URIs

#making a bunch of lists
wikidata_URI_lists = []
wikidata_repeat_uris = []
wikidatacounterlist = []

lc_URI_lists = []
lc_repeat_uris = []
lccounterlist = []

fast_URI_lists = []
fast_repeat_uris = []
fastcounterlist = []

viaf_URI_lists = []
viaf_repeat_uris = []
viafcounterlist = []

#opening the CSV that I exported from OpenRefine and put in Google sheets, to get rid of some extraneous columns
with open ('Reconciliation results analysis_March 2018.csv') as file:
	data = csv.reader(file)
	next(data, None)
	for row in data:
		#make a list for each kind of URI
		wikidata_URI_list = []
		lc_URI_list = []
		fast_URI_list = []
		viaf_URI_list = []

		topicid = row[0]
		lc_URI = row[2]
		fast_URI = row[4]
		viaf_URI = row[6]
		wikidata_URI = row[7]
		#put the wikidata uris in a list I'll pass to the collections Counter later
		wikidatacounterlist.append(wikidata_URI)
		#add the URI and topic id to the list I made earlier in this for loop
		wikidata_URI_list.append(wikidata_URI)
		wikidata_URI_list.append(topicid)
		#add the list just populated with URI and topic id to another list
		wikidata_URI_lists.append(wikidata_URI_list)

		#put the lc uris in a list I'll pass to the collections Counter later
		lccounterlist.append(lc_URI)
		#add the URI and topic id to the list I made earlier in this for loop
		lc_URI_list.append(lc_URI)
		lc_URI_list.append(topicid)
		#add the list just populated with URI and topic id to another list
		lc_URI_lists.append(lc_URI_list)

		#put the lc uris in a list I'll pass to the collections Counter later
		fastcounterlist.append(fast_URI)
		#add the URI and topic id to the list I made earlier in this for loop
		fast_URI_list.append(fast_URI)
		fast_URI_list.append(topicid)
		#add the list just populated with URI and topic id to another list
		fast_URI_lists.append(fast_URI_list)

		#put the lc uris in a list I'll pass to the collections Counter later
		viafcounterlist.append(viaf_URI)
		#add the URI and topic id to the list I made earlier in this for loop
		viaf_URI_list.append(viaf_URI)
		viaf_URI_list.append(topicid)
		#add the list just populated with URI and topic id to another list
		viaf_URI_lists.append(viaf_URI_list)


#figure out which URIs are associated with more than one topic

wikidata_count = count_uris(wikidatacounterlist, wikidata_repeat_uris)
#print(wikidata_count)

lc_count = count_uris(lccounterlist, lc_repeat_uris)
#print(lc_count)

fast_count = count_uris(fastcounterlist, fast_repeat_uris)
#print(fast_count)

viaf_count = count_uris(viafcounterlist, viaf_repeat_uris)
#print(viaf_count)

wikidata_results = result_dictionary(wikidata_URI_lists, wikidata_repeat_uris)
#print(wikidata_results)

lc_results = result_dictionary(lc_URI_lists, lc_repeat_uris)

fast_results = result_dictionary(fast_URI_lists, fast_repeat_uris)

viaf_results = result_dictionary(viaf_URI_lists, viaf_repeat_uris)

with open ('recon_analysis_repeatWikidata_URIs_%s.json' %filetime, 'w') as f:
	json.dump(wikidata_results, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it! Wikidata list made!")

with open ('recon_analysis_repeatLC_URIs_%s.json' %filetime, 'w') as f:
	json.dump(lc_results, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it! LC list made!")

with open ('recon_analysis_repeatFAST_URIs_%s.json' %filetime, 'w') as f:
	json.dump(fast_results, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it! FAST list made!")

with open ('recon_analysis_repeatVIAF_URIs_%s.json' %filetime, 'w') as f:
	json.dump(viaf_results, f, sort_keys=True, ensure_ascii=False, indent=4)
	print("HOORAY, you did it! VIAF list made!")