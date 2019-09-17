import MySQLdb
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import Tkinter

db = MySQLdb.connect(host="localhost",  # your host 
                     user="xxxx",       # username
                     passwd="xxxxx",     # password
                     db="cogs402")   # name of the database
 
# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
cur.execute("select COUNT(*) from dogwood_nb")
size_nb = int(cur.fetchall()[0][0])

cur.execute("select nationbuilder_id, salesforce_id, email, email2, phone_number, mobile_number, primary_zip, address_zip, user_submitted_zip, employer, occupation, recruiter_id, is_volunteer, primary_city, address_city, user_submitted_city, first_name, last_name from dogwood_nb")

# Create empty dogwood_nb matrix
dogwood_nb = np.chararray((size_nb,18), itemsize=100)
row = cur.fetchone()

# Build Dogwood NB supporter network

supporters = nx.Graph()
supporters.clear()

#to keep track of which variables add most edges
emailCount = 0
phoneCount = 0
zipCount = 0
empCount = 0
occCount = 0
volCount = 0

# Populate matrix AND supporter graph nodes
i = 0
while row is not None:
    dogwood_nb[i] = row
    # nationbuilder_id used as node id
    supporters.add_node(dogwood_nb[i][0])
    row = cur.fetchone()
    i += 1

cur.execute("select COUNT(*) from dogwood_sf_test")
size_sf = int(cur.fetchall()[0][0])

# bring in dogwood salesforce contacts
cur.execute("select account_id, contact_id, primary_city, primary_postal, phone, home_phone, other_phone, mobile, email, household_phone, volunteer from dogwood_sf_test") #switch to official sf list

# Create empty dogwood_sf matrix
dogwood_sf = np.chararray((size_sf,11), itemsize=100)
row = cur.fetchone()

# Populate matrix
i = 0
while row is not None:
    dogwood_sf[i] = row
    supporters.add_node(dogwood_sf[i][1])
    row = cur.fetchone()
    i += 1

# Add edges from nb to supporter graph
for i in range (0, size_nb-1):
    a = dogwood_nb[i][0] # nationbuilder_id
    b = dogwood_nb[i][11] # recruiter_id
    if (b == ''):
        b = 0
    
    # Add edge b/w recruiter and supporter once
    if (not supporters.has_edge(a,b) and int(b) != 0):
        supporters.add_edge(*(a,b))
        print('added edge ' + a + ' ' + b)
    
    # Scan rest of nb network for other chances to connect
    for j in range (0, size_nb - 1):
        b = dogwood_nb[j][0] # second node nationbuilder_id

        # Variables for easier readability of conditions below
        emailA = dogwood_nb[i][2]
        emailB = dogwood_nb[j][2]
        email2A = dogwood_nb[i][3]
        email2B = dogwood_nb[j][3]
        phoneA = dogwood_nb[i][4]
        phoneB = dogwood_nb[j][4]
        mobA = dogwood_nb[i][5]
        mobB = dogwood_nb[j][5]
        priZipA = dogwood_nb[i][6]
        priZipB = dogwood_nb[j][6]
        addZipA = dogwood_nb[i][7]
        addZipB = dogwood_nb[j][7]
        useSubZipA = dogwood_nb[i][8]
        useSubZipB = dogwood_nb[j][8]
        empA = dogwood_nb[i][9]
        empB = dogwood_nb[j][9]
        occA = dogwood_nb[i][10]
        occB = dogwood_nb[j][10]
        volA = dogwood_nb[i][12]
        volB = dogwood_nb[j][12]
        priCityA = dogwood_nb[i][13]
        priCityB = dogwood_nb[j][13]
        addCityA = dogwood_nb[i][14]
        addCityB = dogwood_nb[j][14]
        useSubCityA = dogwood_nb[i][15]
        useSubCityB = dogwood_nb[j][15]

        if ((not supporters.has_edge(a,b)) and a != b): # Add edges when: 

            # same email
            if((emailA == emailB or emailA == email2B) and emailA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by emailA')
                print('emailA: ' + emailA)
                emailCount += 1
            elif((email2A == emailB or email2A == email2B) and email2A != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by email2A')
                print('email2A: ' + email2A)
                emailCount += 1
            
            # same phone
            elif((phoneA == phoneB or phoneA == mobB) and phoneA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by phoneA')
                phoneCount += 1
            elif((mobA == phoneB or mobA == mobB) and mobA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by mobA')
                print('mobA: ' + mobA)
                phoneCount += 1
            
            # same zip
            elif((priZipA == priZipB or priZipA == addZipB or priZipA == useSubZipB)
            and priZipA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by priZipA')
                zipCount += 1
            elif ((addZipA == priZipB or addZipA == addZipB or addZipA == useSubZipB) 
            and addZipA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by addZipA')
                zipCount += 1
            elif ((useSubZipA == priZipB or useSubZipA == addZipB or useSubZipA == useSubZipB)
            and useSubZipA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by useSubZipA')
                zipCount += 1
            
            # same employer
            elif(empA == empB and empA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by emp')
                empCount += 1
            
            # same occupation
            elif(occA == occB and occA != ''):
                if (occA == 'Volunteer'):
                    print('added edge ' + a + ' ' + b + 'by occ = Volunteer')
                    if((priCityA == priCityB or priCityA == addCityB or priCityA == useSubCityB)
                    and priCityA != ''):
                        supporters.add_edge(*(a,b))
                        print('added edge ' + a + ' ' + b + 'by priCityA')
                        volCount += 1

                    elif ((addCityA == priCityB or addCityA == addCityB or addCityA == useSubCityB) 
                    and addCityA != ''):
                        supporters.add_edge(*(a,b))
                        print('added edge ' + a + ' ' + b + 'by addCityA')
                        volCount += 1

                    elif((useSubCityA == priCityB or useSubCityA == addCityB or useSubCityA == useSubCityB)
                    and useSubCityA != ''):
                        supporters.add_edge(*(a,b))
                        print('added edge ' + a + ' ' + b + 'by addCityA')
                        volCount += 1
                else:
                    supporters.add_edge(*(a,b))
                    print('added edge ' + a + ' ' + b + 'by occ')
                    print('occ is ' + occA)
                    occCount += 1

            
            # both volunteers in same city
            elif(volA == 'true' and volB == 'true'):
                if((priCityA == priCityB or priCityA == addCityB or priCityA == useSubCityB)
                and priCityA != ''):
                    supporters.add_edge(*(a,b))
                    print('added edge ' + a + ' ' + b + 'by priCityA')
                    volCount += 1

                elif ((addCityA == priCityB or addCityA == addCityB or addCityA == useSubCityB) 
                and addCityA != ''):
                    supporters.add_edge(*(a,b))
                    print('added edge ' + a + ' ' + b + 'by addCityA')
                    volCount += 1

                elif((useSubCityA == priCityB or useSubCityA == addCityB or useSubCityA == useSubCityB)
                and useSubCityA != ''):
                    supporters.add_edge(*(a,b))
                    print('added edge ' + a + ' ' + b + 'by addCityA')
                    volCount += 1

    # Scan SF nodes for chances to connect            
    for k in range(0, size_sf - 1):
        b = dogwood_sf[k][1] # second node sf contact_id
        
        # Variables for easier readability of conditions below
        phoneA = dogwood_nb[i][4]
        phoneB = dogwood_sf[k][4]
        phone2A = dogwood_nb[i][5]
        phone2B = dogwood_sf[k][5]
        phone3B = dogwood_sf[k][6]
        phone4B = dogwood_sf[k][7]
        phone5B = dogwood_sf[k][9]
        priZipA = dogwood_nb[i][6]
        priZipB = dogwood_sf[k][3]
        addZipA = dogwood_nb[i][7]
        useSubZipA = dogwood_nb[i][8]
        volA = dogwood_nb[i][12]
        volB = dogwood_sf[k][10] # this is 0 or 1
        priCityA = dogwood_nb[i][13]
        priCityB = dogwood_sf[k][2]
        addCityA = dogwood_nb[i][14]
        useSubCityA = dogwood_nb[i][15]

        if ((not supporters.has_edge(a,b)) and a != b): # Add edges when: 

            # same phone
            if((phoneA == phoneB or phoneA == phone2B or phoneA == phone3B or phoneA == phone4B or phoneA == phone5B) 
            and phoneA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by phoneA')
                phoneCount += 1
                print('phoneCount = ' + str(phoneCount))
            elif((phone2A == phoneB or phone2A == phone2B or phone2A == phone3B or phone2A == phone4B or phone2A == phone5B)
             and phone2A != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by phone2A')
                print('phone2A: ' + phone2A)
                phoneCount += 1
                print('phoneCount = ' + str(phoneCount))
            
            # same zip
            elif((priZipA == priZipB or addZipA == priZipB or useSubZipA == priZipB)
            and priZipB != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by priZipB')
                print('prizipA = ' + str(priZipA))
                print('addzipA = ' + str(addZipA))
                print('usesubzipA = ' + str(useSubZipA))
                print('zipB = ' + str(priZipB))
                zipCount += 1
                print('zipCount = ' + str(zipCount))
            
            # both volunteers in same city
            elif(volA == 'true' and volB == '1'):
                if((priCityA == priCityB or priCityB == addCityA or priCityB == useSubCityA)
                and priCityB != ''):
                    supporters.add_edge(*(a,b))
                    print('added edge ' + a + ' ' + b + 'by priCityB')
                    volCount += 1  
                    print('volCount = ' + str(volCount))

print('FINISHED NB, adding SF')

#to keep track of which variables add most edges
emailCount2 = 0
phoneCount2 = 0
zipCount2 = 0
volCount2 = 0

# Now connect SF nodes to each other
for i in range (0, size_sf-1):
    a = dogwood_sf[i][1] # sf contact_id
    
    # Scan rest of nb network for other chances to connect
    for j in range (0, size_sf - 1):
        b = dogwood_sf[j][1] # second node sf contact_id
        # Variables for easier readability of conditions below
        emailA = dogwood_sf[i][8]
        emailB = dogwood_sf[j][8]
        phoneA = dogwood_sf[i][4]
        phoneB = dogwood_sf[j][4]
        phone2A = dogwood_sf[i][5]
        phone2B = dogwood_sf[j][5]
        phone3A = dogwood_sf[i][6]
        phone3B = dogwood_sf[j][6]
        phone4A = dogwood_sf[i][7]
        phone4B = dogwood_sf[j][7]
        phone5A = dogwood_sf[i][9]
        phone5B = dogwood_sf[j][9]
        postalA = dogwood_sf[i][3]
        postalB = dogwood_sf[j][3]
        volA = dogwood_sf[i][10]
        volB = dogwood_sf[j][10] #this is 0 or 1
        priCityA = dogwood_sf[i][2]
        priCityB = dogwood_sf[j][2]

        if ((not supporters.has_edge(a,b)) and a != b): # Add edges when: 

            # same email
            if(emailA == emailB and emailA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by emailA')
                print('emailA: ' + emailA)
                emailCount2 += 1
                print('emailCount2 = ' + str(emailCount2))
            
            # same phone
            elif((phoneA == phoneB or phoneA == phone2B or phoneA == phone3B or phoneA == phone4B or phoneA == phone5B) 
            and phoneA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by phoneA')
                phoneCount2 += 1
                print('phoneCount2 = ' + str(phoneCount2))
            elif((phone2A == phoneB or phone2A == phone2B or phone2A == phone3B or phone2A == phone4B or phone2A == phone5B)
             and phone2A != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by phone2A')
                phoneCount2 += 1
                print('phoneCount2 = ' + str(phoneCount2))
            elif((phone3A == phoneB or phone3A == phone2B or phone3A == phone3B or phone3A == phone4B or phone3A == phone5B)
             and phone3A != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by phone3A')
                phoneCount2 += 1
                print('phoneCount2 = ' + str(phoneCount2))
            elif((phone4A == phoneB or phone4A == phone2B or phone4A == phone3B or phone4A == phone4B or phone4A == phone5B)
             and phone4A != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by phone4A')
                phoneCount2 += 1
                print('phoneCount2 = ' + str(phoneCount2))
            elif((phone5A == phoneB or phone5A == phone2B or phone5A == phone3B or phone5A == phone4B or phone5A == phone5B)
             and phone5A != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by phone5A')
                phoneCount2 += 1
                print('phoneCount2 = ' + str(phoneCount2))
            
            # same zip
            elif(postalA == postalB and postalA != ''):
                supporters.add_edge(*(a,b))
                print('added edge ' + a + ' ' + b + 'by postA')
                zipCount2 += 1
                print('zipCount2 = ' + str(zipCount2))
            
            # both volunteers in same city
            elif(volA == '1' and volB == '1'):
                if(priCityA == priCityB and priCityA != ''):
                    supporters.add_edge(*(a,b))
                    print('added edge ' + a + ' ' + b + 'by priCityA')
                    volCount2 += 1  
                    print('volCount2 = ' + str(volCount2))


print('Nodes: ' + str(supporters.number_of_nodes()))
print('Edges: ' + str(supporters.number_of_edges()))

print(str(emailCount) + ' edges by email')
print(str(phoneCount) + ' edges by phone')
print(str(zipCount) + ' edges by zip')
print(str(empCount) + ' edges by emp')
print(str(occCount) + ' edges by occ')
print(str(volCount) + ' edges by vol')

nx.write_gml(supporters, 'dogwood_nb_supporters.gml')
nx.write_adjlist(supporters, 'dogwood_nb_supporters.adjlist')
nx.write_edgelist(supporters, 'dogwood_nb_supporters.edgelist')