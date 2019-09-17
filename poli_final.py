import MySQLdb
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import Tkinter

db = MySQLdb.connect(host="localhost",  # your host 
                     user="xxxxxx",       # username
                     passwd="xxxxxxxxx",     # password
                     db="cogs402")   # name of the database
 
# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
cur.execute("select COUNT(*) from current_MP_meetings_twitter")
size_meetings = int(cur.fetchall()[0][0])
cur.execute("select id,REPLACE(last_name, ' ', ''),REPLACE(first_name, ' ', ''), twitter_handle from current_MP_meetings_twitter")

print(size_meetings)

# Create empty matrix
meetings = np.chararray((size_meetings,4), itemsize=100)
print(len(meetings))
row = cur.fetchone()

# Populate matrix
i = 0
while row is not None:
    meetings[i] = row
    row = cur.fetchone()
    i += 1

# Build politician network

cur.execute("select distinct REPLACE(last_name, ' ', ''),REPLACE(first_name, ' ', ''), twitter_handle from current_MP_meetings_twitter where last_name != 'stephane' AND last_name != 'duvall' AND last_name != 'fortin' AND last_name != 'hussen'")

reps = nx.Graph()
reps.clear()

# Add nodes to reps graph
i = 0
row = cur.fetchone()
while row is not None:
    if row[2] != 'NULL':
        reps.add_node(row[2])
    else:
        reps.add_node(row[0]+row[1])
        print('NULL: ' + row[0] + row[1])
    row = cur.fetchone()
    i += 1

# Add edges with weights to reps graph - more edges than necessary
for i in range (0, size_meetings-1):
    j = i + 1
    
    while (meetings[i][0] == meetings[j][0]):
        a = meetings[i][3]
        b = meetings[j][3]
        
        if (not reps.has_edge(a,b)): # Only add each edge once
            reps.add_edge(*(a,b),weight=1)
            
        else:
            weight = reps[a][b]['weight'] # Increase weight of edge every time a meeting b/w 2 reps is repeated
            reps[a][b]['weight'] += 1
            
        j += 1

# Prune network so only reps that have met more than 4 times remain connected
edges = reps.edges()
to_remove = []

print(reps.number_of_edges())

for e in edges:
    if (reps.get_edge_data(*e)['weight'] < 3):
        to_remove.append(e)

reps.remove_edges_from(to_remove)

print(reps.number_of_nodes())
print(reps.number_of_edges())
print(reps.nodes())

nx.write_gml(reps, 'poli_final.gml')
nx.write_adjlist(reps, 'poli_final.adjlist')
nx.write_edgelist(reps, 'poli_final.edgelist')