import MySQLdb
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import Tkinter

db = MySQLdb.connect(host="localhost",  # your host 
                     user="xxxx",       # username
                     passwd="xxxxxx",     # password
                     db="cogs402")   # name of the database
 
# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
cur.execute("select COUNT(*) from leap_supporters")
size_en = int(cur.fetchall()[0][0])

cur.execute("select supporter_id, email_address, telephone, address_1, postcode from leap_supporters")

# Create empty dogwood matrix
leap = np.chararray((size_en,5), itemsize=100)
row = cur.fetchone()

# Build The Leap supporter network

supporters = nx.Graph()
supporters.clear()

# Populate matrix AND supporter graph nodes
i = 0
while row is not None:
    leap[i] = row
    # supporter_id used as node id
    supporters.add_node(leap[i][0])
    row = cur.fetchone()
    i += 1

#to keep track of which variables add most edges
emailCount = 0
phoneCount = 0
addCount = 0
postCount = 0

# Add edges to supporter graph
for i in range (0, size_en-1):
    a = leap[i][0] # supporter_id
    
    # Scan supporter list for chances to connect
    for j in range (0, size_en - 1):
        b = leap[j][0] # second node supporter_id

        # Variables for easier readability of conditions below

        emailA = leap[i][1]
        emailB = leap[j][1]
        phoneA = leap[i][2]
        phoneB = leap[j][2]
        addA = leap[i][3]
        addB = leap[j][3]
        postA = leap[i][4]
        postB = leap[j][4]


        if ((not supporters.has_edge(a,b)) and a != b): # Add edges when: 

            # same email
            if(emailA == emailB and emailA != ''):
                supporters.add_edge(*(a,b))
                print('countPhone = ' + str(emailCount))

            # same phone
            elif(phoneA == phoneB and phoneA != ''):
                supporters.add_edge(*(a,b))
                print('countPhone = ' + str(phoneCount))
            
            # same postal code
            elif(postA == postB and postA != ''):
                supporters.add_edge(*(a,b))
                print('countPhone = ' + str(postCount))
            
            # same address
            elif(addA == addB and addA != ''):
                supporters.add_edge(*(a,b))
                print('countPhone = ' + str(addCount))

print('Nodes: ' + str(supporters.number_of_nodes()))
print('Edges: ' + str(supporters.number_of_edges()))

nx.write_gml(supporters, 'leap_supporters.gml')
nx.write_adjlist(supporters, 'leap_supporters.adjlist')
nx.write_edgelist(supporters, 'leap_supporters.edgelist')
