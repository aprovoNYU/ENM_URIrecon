

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

if "human" in schemaPerson_list:
    print ("schema:Person")