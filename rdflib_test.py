from rdflib import Graph

g = Graph()
g.parse("demo.nt", format="nt")

len(g) # prints 2

import pprint
for stmt in g:
    pprint.pprint(stmt)

g.parse("http://experimental.worldcat.org/fast/1736774/rdf.xml")
print(len(g))
# prints 42