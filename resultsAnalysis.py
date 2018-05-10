import json
#import xml.etree.ElementTree as ET


def results_Analysis(filename):
	
	#from https://www.pythoncentral.io/how-to-check-if-a-list-tuple-or-dictionary-is-empty-in-python/
	def is_empty(any_structure):
		if any_structure:
		#print('Structure is not empty.')
			return False
		else:
		#print('Structure is empty.')
			return True

	urisadded = []
	typesadded =[]
	typelistsadded = []
	with open (filename) as json_data:
		topics = json.load(json_data)
		for topic in topics:
			uri = topic["external_link"]["URL"]
			urisadded.append(uri)
			try: 
				topic_typelist=topic["external_link"]["recon_data"]["topic_type"]
				typelistsadded.append(topic_typelist)

				#print(topic_typelist)

				for x in topic_typelist:
					typesadded.append(x)
			except:
				#print("topic had no types")
				pass

	print("URIs added: ")
	if is_empty(urisadded) == False:
		for idx, item in enumerate(urisadded):
			uriresult = (idx+1, item)
	print(uriresult)

	print("Types added:")
	if is_empty(typesadded) == False:
		for idx, item in enumerate(typesadded):
			try:
				typesaddedresult = (idx+1, item)
			except:
				"Error, no types present"
		print(typesaddedresult)
	
	print("Type lists added:")
	if is_empty(typelistsadded) == False:
		for idx, item in enumerate(typelistsadded):
			typelistsaddedresult = (idx+1, item)
	print(typelistsaddedresult)



filename = input("enter file name to analyze: ")
results_Analysis(filename)