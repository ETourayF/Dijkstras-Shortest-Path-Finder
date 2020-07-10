infinity = 1000000
invalid_node = -1


class Node:
    previous = invalid_node
    distancefromsource = infinity
    visited = False


class Dijkstra:
    
    def __init__(self):
        self.startnode = 0
        self.endnode = 0

        self.network = []
        self.network_populated = False
        
        self.nodetable = []
        self.nodetabelpopulated = False

        self.route = []
        self.route_populated = False

        self.currentnode = 0

    '''populates the node table'''
    def populate_node_table(self):
        for line in self.network:
            self.nodetable.append(Node())

        self.nodetable[self.startnode].distancefromsource = 0
        self.nodetable[self.startnode].visited = True
        self.nodetablepopulated = True

    def populate_network(self, filename):
        '''load csv file from current directory'''
        self.network_populated = False

        '''ensure file exists before attempting to open'''
        try:
            networkFile = open(filename, "r")

        except IOError:
            print("network file does not exist!")
            return
        
        for line in networkFile:
            self.network.append(list(map(int, line.strip().split(","))))

        self.network_populated = True
        networkFile.close()

    def parse_route(self, filename):
        '''load in route file'''
        self.route_populated = False

        try:
            routefile = open(filename, "r")

        except IOError:
            print("route file does not exist!")
            return
        
        route = routefile.read()
        route = route.strip().split(">")

        '''get nemerical values of start and end node'''
        self.startnode = ord(route[0]) - 65
        self.endnode = ord(route[1]) - 65
        
        #print (self.startnode)
        #print (self.endnode)
       
        self.route_populated = True
        routefile.close()
        
    def return_near_neighbour(self):

        return_List = []

        '''parse the network data structure and return a list of unvisited near neighbours of the current node'''
        
        for index, value in enumerate(self.network[self.currentnode]):
            if value > 0 and not self.nodetable[index].visited:
                return_List.append(index)
       
        return return_List

    def calculate_tentative(self):
        '''calculate tentative distances of nearest neighbours'''
        
        '''create a list of the nearest neighbours of the current node'''
        nn = self.return_near_neighbour()
        
        for neighbour in nn:
            #fix comment
            '''find the position of each neighbour in the networks graph'''
            initial_distance = self.network[self.currentnode][neighbour]
            
            '''if distance of source of the neighbour is unchanged'''
            if(self.nodetable[neighbour].distancefromsource == infinity):
                '''previous node for the each neighbour is the current node (from which we're checking)'''
                self.nodetable[neighbour].previous = self.currentnode
                '''distance from source for neighbour is the sum of 'current_nodes distance from source' and the neighbours 'distance of source'''
                self.nodetable[neighbour].distancefromsource = self.nodetable[self.nodetable[neighbour].previous].distancefromsource + initial_distance

            elif(self.nodetable[neighbour].distancefromsource > self.nodetable[self.currentnode].distancefromsource + initial_distance):
                '''previous node for the each neighbour is the current node (from which we're checking)'''
                self.nodetable[neighbour].previous = self.currentnode
                '''distance from source for neighbour is the sum of 'current_nodes distance from source' and the neighbours 'distance of source'''
                self.nodetable[neighbour].distancefromsource = self.nodetable[self.currentnode].distancefromsource + initial_distance

    
    '''finction determines the next node to visit'''
    def determine_next_Node(self):
        '''get all near neighbours of current node'''
        nn = self.return_near_neighbour()
        
        smallest_distance = infinity
        next_node = 0

        '''go through list of near neighbours'''
        for neighbour in nn:
            '''variable to hold distance of source of current neighbour'''
            nDistance = self.nodetable[neighbour].distancefromsource
            
            '''check if neighbour has smaller distance than current smallest distance'''
            if nDistance < smallest_distance:
                '''set a new smallest distance, and set the neighbour as the next node to visit'''
                smallest_distance = self.nodetable[neighbour].distancefromsource
                next_node = neighbour

        return next_node
    
    def calculate_shortest_path(self):
        '''unvisited node list'''
        u_nodes_list = list(range(len(self.nodetable)))

        '''returns list of unvisited near neighbours - this initially is all of them'''
        nn = self.return_near_neighbour()

        while (True):
            '''ensures that there aren't any unvisted unvisited node once destination is found'''
            if (len(nn) == 0 and len(u_nodes_list) != 0):
                '''set current node to visited and remove it from the list'''
                self.nodetable[self.currentnode].visited = True
                u_nodes_list.remove(self.currentnode)
                self.currentnode = u_nodes_list[0]

            elif (len(nn) == 0 and len(u_nodes_list) == 0):
                '''if all nodes and near neighbours have been visited then
                set current node to visited and end the loop'''
                self.nodetable[self.currentnode].visited = True
                return

            '''get tentative distance of current node and mark it as visited'''
            self.calculate_tentative()
            self.nodetable[self.currentnode].visited = True
            '''once visited remove it from list of unvisited nodes'''
            u_nodes_list.remove(self.currentnode)
            '''determine which node to go to next'''
            self.currentnode=self.determine_next_Node()
            '''retrieve near neighbours of the new node'''
            nn = self.return_near_neighbour()
    
    def return_shortest_path(self):
        '''calculate shortest path between start and end node'''
        self.calculate_shortest_path()
        node_tmp = self.endnode
        '''total distance'''
        distance_sum = self.nodetable[self.endnode].distancefromsource

        '''shortest path'''
        s_path = []
        s_path.append(self.endnode)

        while(self.nodetable[node_tmp].previous != invalid_node):
            s_path.insert (0, self.nodetable[node_tmp].previous)
            node_tmp = self.nodetable[node_tmp].previous
        
        s_path.append(distance_sum)

        print("Shortest Path:")
        for item in s_path[:-1]:
            print(chr(item + 65))
    
        print("Total Distance: " + str(s_path[-1]))


        return s_path

if __name__ == '__main__':
    Algorithm = Dijkstra()
    Algorithm.populate_network("network.txt")
    Algorithm.parse_route("route.txt")
    Algorithm.currentnode = Algorithm.startnode
    Algorithm.populate_node_table()
    print("Network Table:")
    for line in Algorithm.network:
        print(line)
    print(f"Startnode = {Algorithm.startnode}, Endnode = {Algorithm.endnode}")

    Algorithm.return_shortest_path()

