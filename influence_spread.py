#!/usr/bin/env python2
# -*- coding: latin-1 -*-
import MySQLdb
import csv
import networkx as nx
import numpy as np
from collections import defaultdict

db = MySQLdb.connect(host="localhost",  # your host 
                     user="xxxxx",       # username
                     passwd="xxxxxxx",     # password
                     db="cogs402")   # name of the database

def get_avg_inf_spread(net, table, flag):
    print(table)
    if flag == 'pol':
        x = 0.01
    elif flag == 'sup':
        x = 0.1 
    inf_mat = get_inf_mat(net, table, x, flag)
    totals = inf_mat[0]
    size_totals = len(totals)

    credit = 0
    for i in range(0, size_totals):
        print('Total credit distributed, nodes credited = ' + str(totals[i]))
        credit += totals[i][0]
    
    avg = credit/size_totals
    print('Average influence spread = ' + str(avg))

    return avg

def get_inf_mat(net, table, thresh, flag):
    #list of all actions in action trace
    a_list = get_a_list(table, flag)
    active_nodes = get_active_nodes(table, flag)
    print('active nodes = ' + str(len(active_nodes)))

    #array holds adjlists for all actions
    uc_arr = [] #each index is one action, and [0] of THAT is total credit granted, [1] is b/w how many nodes

    for a in a_list:
        #adjlist that has all edges in our graph - will add weights that correspond to influence credit
        uc = net
        total_credit = 0
        total_nodes_credited = 0
        if flag == 'sup':
            a = a[0]
        print('in action ' + a)
        #action trace for action a
        at = get_at(table, a, flag)
        #keeps track of users seen so far for this action
        curr_tab = []
        print(uc.nodes())

        for sub in at:
            if flag == 'sup':
                u = sub[2] # supporter_id
            elif flag == 'pol':
                u = sub[3]
            parents = []
            if net.has_node(u):
                print('scanning ' + str(u))

                uc.nodes[u]['propagation'] = 0
                uc.nodes[u]['totalcredit'] = 0
            
                neighbors = net.neighbors(u)

                # will only add parents in regard to action if we've seen the nodes before - scanning in chrono order
                for i in neighbors:
                    # initialize uc
                    uc[i][u]['credit'] = 0

                    if i in curr_tab:
                        parents.append(i)
                        print('added node ' + str(i) + ' to parents')
                
                if len(parents) > 0:
                    credit = (1.0/len(parents))

                for v in parents:
                    if credit >= thresh:
                        # give v credit for influencing u
                        print('granting ' + str(credit) + ' credit to node ' + str(v))
                        prev_credit = uc[v][u]['credit']
                        uc[v][u]['credit'] = prev_credit + credit

                        uc.nodes[v]['propagation'] += 1
                        uc.nodes[v]['totalcredit'] += credit

                        total_credit += credit
                        total_nodes_credited += 1
                        
                        v_neighbors = net.neighbors(v)
                        v_parents = []
                        for node in v_neighbors:
                            if node in curr_tab:
                                v_parents.append(node)


                        # give parents of v credit for influencing u
                        for w in v_parents:
                            if ((uc[w][v]['credit'] * credit) >= thresh) & (u != w):
                                if net.has_edge(w, u):
                                    print('granting ' + str(credit) + ' credit to parent of v ' + str(w))
                                    prev_credit = uc[w][u]['credit']
                                    uc[w][u]['credit'] = prev_credit + (credit * uc[w][v]['credit'])
                                else:
                                    print('granting ' + str(credit) + ' credit to parent of v' + str(w))
                                    uc.add_edge(w,u)
                                    uc[w][u]['credit'] = credit * uc[w][v]['credit']
                                
                                uc.nodes[w]['propagation'] += 1
                                uc.nodes[w]['totalcredit'] += credit * uc[w][v]['credit']
                                total_credit += credit
                                total_nodes_credited += 1


                curr_tab.append(u)
                
        # save a few versions of uc we created
        nx.write_gml(uc, 'uc_' + a + '.gml')
        nx.write_adjlist(uc, 'uc_' + a + '.adjlist')
        nx.write_edgelist(uc, 'uc_' + a + '.edgelist')
        # add totals
        arr = [total_credit, total_nodes_credited]
        uc_arr.append(arr)


    return [uc_arr, uc]

def get_active_nodes(table, flag):
    cur = db.cursor()
    if (flag == 'sup'):
        cur.execute("select distinct supporter_id from " + table)
        row = cur.fetchone()

        node_list = []
        while row is not None:
            node_list.append(row)
            row = cur.fetchone()

    elif (flag == 'pol'):
        cur.execute("select distinct handle from twitter_handles")
        row = cur.fetchone()

        node_list = []
        while row is not None:
            node_list.append(row)
            row = cur.fetchone()

    return node_list

def get_a_list(table, flag):
    if (flag == 'sup'):
        cur = db.cursor()
        cur.execute("select distinct c_name from " + table)
        row = cur.fetchone()

        a_list = []
        while row is not None:
            a_list.append(row)
            row = cur.fetchone()

    elif (flag == 'pol'):
        a_list = ['tweets']
    
    return a_list

def get_at(table, col, flag):
    if (flag == 'sup'):
        # fetch data from MySQL
        cur = db.cursor()
        cur.execute("select count(*) from " + table)
        size_tab = int(cur.fetchall()[0][0])
        cur.execute("select c_name, sub_datetime, supporter_id from " + table + " where c_name = '" + col + "' order by sub_datetime") # maybe order by c_name to optimize?
        
        mat = np.chararray((size_tab,3), itemsize=100)

        row = cur.fetchone()

        # populate matrix
        i = 0
        while row is not None:
            mat[i] = row
            row = cur.fetchone()
            i += 1
    
        cur.close()

    elif (flag == 'pol'):
        # load data from npy array
        mat = np.load('poli_at.npy')
        print('size of poli at is: ' + str(len(mat)))
    
    return mat


# Driver code 
if __name__ == '__main__': 
    dogwood = nx.read_adjlist('dogwood_pruned_supporters.adjlist')
    leap = nx.read_adjlist('leap_supporters.adjlist')
    poli = nx.read_adjlist('poli_final.adjlist')

    dogwood_inf = get_avg_inf_spread(dogwood, 'dogwood_full_at', 'sup')
    leap_inf = get_avg_inf_spread(leap, 'leap_at_clean', 'sup')
    poli_inf = get_avg_inf_spread(poli, '', 'pol')