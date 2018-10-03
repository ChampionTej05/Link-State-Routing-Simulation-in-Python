# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 16:50:40 2018

@author: champion
"""



import os



######################################################################################################################################

# Information

######################################################################################################################################





# Description :

"""

    The program accepts the network topology details in terms of the cost of links, and provides the shortest path tree for the

    network. It uses Dijkstra's Algorithm to construct its routing table.

"""



# Logic :

"""

    1. The program first asks for a network topology file. It validates the data and

       store in matrix format.

    2. The next step is to create the connection table. The program takes the source

       router as input, and performs the Dijkstra Algorithm on it.

    3. For Dijkstra Algorithm, the program follows below steps:

        A. It selects the source node as the root of the tree and add it to the path.

           Then it sets the shortest distances for all the neighbors of the root to the cost

           between the root and those neighbors. Finally it sets the shortest distance of the root to zero.

        B. Then it repeats the following two steps in loop until all nodes are added to the path:

            a. It searches the for nodes which are not in the path. It then selects the one with minimum shortest distance and add it to the path.

            b. It updates the shortest distance for all remaining nodes using the shortest distance of the node just moved to the path in previous step.

    4. At every step, it keeps track of two type of nodes:

        A. The interface used to go to next router. (For connection table.)

        B. The parent node of last added node. (To create the final path.)

    5. Once both connection table and parent table are ready, the shortest path is

       found from given source to destination by following way :

        A. Starting from the destination node, it follows the parent node from the parent

           table to reach to the source, and provide the reverse path.

        B. The total cost is found by adding the cost of all the nodes in previous step.

    6. If there is no path from given source and destination, the program returns with

       such message.

    

"""





# Run Instructions :

"""

    Run the program by command : python lsp_project.py

    
    Select the commands in Sequence 
    
    Please use the text file for input, store the values in Matrix format
    
    Value=-1, shows no Link, postive values indicates the cost of link
	
	Two input files are already provided in the folder, please make use of that. 
    

"""

#Algorithm of Link State Routing:

"""
    1. Every Router Builds Initial Routing Table, according to the Information received from the Neighbour, Achieved through set_distances() method
    
    2. Flooding the LSP(Intial Routing Tables) to the All the Routers, We have used simple logic to share the information to all the routers.
        We have made the Routing tables global due to which it will be shared by default between the Routers.
        This Technique is less accurate but more efficient instead of using the Flooding to flood packets.
        
    3. Formation of Shortest Path Tree, we take the Source Router and then find the shortest path from source to 
        all the other routers,using the information it has received from the neighbours.
        
    4. Calculate the Routing table to reach to Destination.

"""





# Initialization of all the variables.



router_matrix = []  #contains the Cost matrix for the Routers

matrix_set = 0  #used to check if the data is set or not

nodes = []

#dictionaries used during Dijkistra Algorithm
distances = {}

unvisited = {}

previous = {}

visited = {}

interface = {}

#stores the path from source node to destination node 
path = []

start = 0

end = 0

numnodes=0



# Function to print the choices when program starts.



def print_choices():



    print ("######################################################")

    print ("\nCN 317 Link State Routing Simulator\n")

    print ("(1) Input Network Topology File")

    print ("(2) Build a Connection Table")

    print ("(3) Shortest Path to Destination Router")

    print ("(4) Exit")

    print ("\n######################################################\n")

    pass





# Function to check if entered command is valid or not - i.e. :

# 1: Should be a digit.

# 2: Should be from the range of given choices.





def check_choices(command):

    

    if not command.isdigit():

        print ("Please enter a number as command from given choices..")

        return -1

    else:

        command = int(command)

        

        if command > 4 or command < 1 :

            print ("Please enter a valid command from given choices..")

            return -1

        else:

            return command





# Function to process the given input file.





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
        
        print("--------------------")
        
        for key,value in distances.items():
            print(key,value)
        
        print("---------------------")
            

def show_Values(c):
    print(" ")
    print("#################",c)
    print("---Unvisited Dict---")
    
    for k,v in unvisited.items():
        print (k,v)
        
    print("----------------------")
    
    print("----Previous Dict -----")
    for k,v in previous.items():
        print (k,v)
    
    print("----------------------")
    
    print("-----Interface Dict -------")
    for k,v in interface.items():
        print (k,v)
    
    print("----------------------")

    print("----Visited Dict-------")
    for k,v in visited.items():
        print (k,v)
    
    print("----------------------")
    print(" ")
    print("#################",c)
    


def dijkstra(start):



    global distances

    global nodes

    global unvisited

    global previous

    global visited

    global interface          #store a particular node can be reached from source node via which interface,
                                # ex: interface[5]=1 implies that 5 can be reached from src=2 through neighbour 1



    # set the values to none for initialization.

    

    unvisited = {node: None for node in nodes}

    previous = {node: None for node in nodes}

    interface = {node: None for node in nodes}

    visited = {node: None for node in nodes}



    current = start

    currentDist = 0
    
    #setting the Cost to Start node=0
    unvisited[current] = currentDist

    print("Building the Router Table for Router:",start)

    while True:

        #show_Values(0)
        for next, distance in distances[current].items():

            #print("Next value is :",next)
            #if the node is visited already, do nothing
            if next not in unvisited: continue

            

            newDist = currentDist + distance


            #setting up the parent, for the shortest node/router
            if not unvisited[next] or unvisited[next] > newDist:
                
                unvisited[next] = newDist

                previous[next] = current

                

                if not interface[current]:

                    interface[next] = next
                   # print("in IF ")

                else:

                    interface[next] = interface[current]
                   # print("in ELSE")
                #show_Values(1)

                    
        #adding the Current node to Closed List
        visited[current] = currentDist

        #removing current node from list of Unvisited Nodes
        del unvisited[current]

        
        #to Check at least one node is left to explore
        shallWeStop = 1

        for x in unvisited:

            if unvisited[x]:

                shallWeStop = 0

                break

        #stop the iteration if no unvisited nodes
        if not unvisited or shallWeStop:

            break



        #store the all neighbours of the CUrrent node
        elements = [node for node in unvisited.items() if node[1]]

#        print("Elements ....")
#        
#        for element in elements:
#            print(element)
#            
#        print(".................")

        #get the node with least distance
        #it will be the next processing node
        current, currentDist = sorted(elements, key = lambda x: x[1])[0]
#        print("Current =",current)
#        print("Current Dist=",currentDist)
#        
#        print("**************************************")





# Function to generate the shortest path using the parent table generated by function dijkstra.





def shortest_path(start, end):

    

    global path



    path = []
    
    

    dest = int(end)

    src = int(start)

    path.append(dest)



    while dest != src:

        path.append(previous[dest])

        dest = previous[dest]



    path.reverse()



#----------------------------------------------------------------------------#

# Actual Program Starts

#----------------------------------------------------------------------------#







command = 0





# Run till user wants to exit.



while command !=4 :


    print_choices()
    command = check_choices(input("\nCommand : "))

    

    # Accept the topology file.

    

    if command == 1:

        

        if matrix_set == 1:

            answer = input("\nThe network topology is already uploaded. Do you want to overwrite? (Y/N) :")



        if matrix_set == 0 or answer == 'Y' or answer == 'y':

        

            filename = input("\nInput original network topology matrix data file[ NxN distance matrix. (value : -1 for no link, 0 for self loop) : ")



            if os.path.isfile(filename):

                process_file(filename)

                start = 0

                end = 0

            else:

                print ("\nThe file does not exist. Please try again..")



    # Accept the source router and display the connection table.



    elif command == 2:

        

        if matrix_set == 1 :

            
            for i in range(1,len(nodes)+1):
                start=i
                
                
                #run for each Router
                dijkstra(start)
                
                print("---------------------------------")
                print("Routing Table For:",start)
                print ("\nDestination\tInterface")

                for key in interface:

                    print (key,"\t\t", interface[key])
                    
                print("---------------------------------")
    
                



        else:

            print ("\nNo network topology matrix exist. Please upload the data file first.. ")



    # Accept the destination router and display the shortest path and cost.



    elif command == 3:

    

        if matrix_set == 1 :


            start=input("\nSelect Start Router:")
            end = input("\nSelect a destination router : ")

            
            dijkstra(int(start))
            if end.isdigit() and int(end) > 0 and int(end) <= len(router_matrix):

                if int(start) == 0:

                    print ("\nNo source router selected yet. Please select a source router using choice : 2.")

                elif int(start) == int(end):

                    print ("\nSource and Destination routers are same. Please select a different destination router.")

                elif not previous[int(end)] :

                    print ("\nThere does not exist any route from Source : {} to Destination : {}. \nPlease select a different destination router. ".format('start','end'))

                else:

                    shortest_path(start,end)

                    print ("\nThe shortest path from router %s to router %s : " %(start,end)),

                    for item in path:

                        print (str(item) + '  '),

                    print ('')

                    cost = 0

                    if visited[int(end)]:

                        cost = visited[int(end)]

                    print ("\nThe total cost is : ",  cost)

        

            else:

                print ("\nPlease enter a valid destination router.")



            pass





        else :

            print ("\nNo network topology matrix exist. Please upload the data file first.. ")
     #Exit if command is 4.       
    else:
          print ("\n Simulation END....\n")







      