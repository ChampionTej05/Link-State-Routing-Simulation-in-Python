# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 20:51:38 2018

@author: champion
"""
import os


"""

Instructions:
    1. You can choose the provided input files to run the program.
    2. Please provide the valid path for the input file to run the algorithm
    3. Do not put any negative edge weights other than "-1" cause connection link never have 
        negative cost associated with them. "-1" here suggests absence of link in the network.

"""

"""
    Algorithm:
        1. Build the Connection between the Routers first
        2. Build the Connection link list present in the network.
        3. Run the Bellman ford for each router to find out the shortest distance to all the other nodes from it.
        4. Bellman Ford Algorithm:
            a. Intialize the distance matrix to all the routers to INF, dist[i] refers to distance to reach router i from src.
            b. Make the distance to reach the source=0
            c. There will be at max (Nodes-1) no of links between a node and source. So run the loop (Nodes-1) times.
                A. Each iteration i denotes the no of links required to reach to that particular node.
                B. In each iteration, check for every edge, is there any better path to reach node that current path,
                    with "i" no of links. If yes, update the distance and save the next hop else ignore.
            d. At the end print all the distances from source to destination along with next hop.
            
        

"""

router_matrix = []  #contains the Cost matrix for the Routers

nodes = []

#dictionaries used during  Algorithm
distances = {}
num_nodes=0

edges=[]       #used to store all the edges:

def process_file(fname):

    

    global matrix_set

    global router_matrix
    

    matrix_set = 0

    router_matrix = []



    with open(fname) as f:

        router_matrix=[list(map(int,x.split(" "))) for x in f]      # Data from input file is stored in a two dimensional list(array).

    matrix_set = 1



    print ("\nReview original topology matrix:\n")

    for line in router_matrix :

        for item in line :

            print (item,end=" ")

        print(" ")

    print



    set_distances(router_matrix)        # Distances are stored in a dictionary - key,value pair - with source router as key and distances in form of a dictionary as value.





# Function to store the distances in dictionary format.





def set_distances(router_matrix):



    global distances

    global nodes
    
    

    

    distances = {}

    nodes = []



    num_nodes = len(router_matrix)
    

    print ("Creating Routing Tables ... ")

    for i in range(num_nodes):

        tempdict = {}

        for j in range(num_nodes):

            if i!=j and router_matrix[i][j]!=-1:

                tempdict[j+1] = router_matrix[i][j]

        distances[i+1] = tempdict

        nodes.append(i+1)
    
    set_edges()
        
   
#makes the list of edges present in the graph     
def set_edges():
    print("--------------------")
    print("U","V","W")
    for key,value in distances.items():
        u=key
        value=dict(value)
        for v,wt in value.items():
            print(u,v,wt)
            edges.append([u,v,wt])
            
    
    print("---------------------")
        
def bellman_ford(src):
   
    global nodes
    

    #local previous dict which would store the next hopes for the source
    nextHop={}
    
    nextHop={node: None for node in nodes}
    
    num_of_nodes=len(router_matrix)
#    print("No of Nodes= ",num_of_nodes)
    
    #intialize dist to all as infinity and dist to src =0
    dist = [float("Inf")] * (num_of_nodes+1) 
    dist[src] = 0
    
    for i in range(num_of_nodes -1):
        #take each edge and check for the each edge in the edge list
        for u,v,wt in edges:
#            print("Edge Considered is: ",u,v,wt)
            if dist[u]!= float("Inf") and dist[u]+wt<dist[v]:
                dist[v]=dist[u]+wt
                
                if not nextHop[v]:
                    nextHop[v]=v
#                    print("In Inner IF...")
                
                else:
#                    print("In Inner ELSE....")
                    nextHop[v]=nextHop[u]
            
#            print("Distance Matrix..")
#            for i in dist:
#                print(i)
#            
#            print("Next Hop...")
#            for k,v in nextHop.items():
#                print(k,v)
#            
#            print("----------------------------------------")
        
    
    print("Table for Router : ",src)
    print("Destination \t Next Hop \t Distance")
    
    destination_list=list()
    nextHop_list=list()
    
    #add just one intial default value to both list so that, as we need to print 
    #it along with dist matrix where first value in INF always, we can use same index to print.
    
    destination_list.append(999)
    nextHop_list.append(999)
    for k,v in nextHop.items():
        if v==None:
            v=src
        destination_list.append(k)
        nextHop_list.append(v)
    
    for i in range(1,num_of_nodes+1):
        print("%d \t\t %d \t\t %d" %(destination_list[i],nextHop_list[i],dist[i]) )
                
#main Program starts here.
filename=input('Enter FileName: ')
if os.path.isfile(filename):
    process_file(filename)
else:
    print('File Does not Exists\n')

numof_nodes=len(router_matrix)
#setting up the table for each router
for i in range(1,numof_nodes+1):
    bellman_ford(i)