import sys 
  




class Graph(): 
  
    def __init__(self, node_list): 
        self.node_list = node_list
        self.sptSet = []
        
    def get_distance(self, node1, node2):
        if node1 == node2:
            return -1
        elif node1.type == 'router' and node2.type == 'router':
            return 1e-10
        else:
            xc1,yc1 = node1.get_center() 
            xc2,yc2 = node2.get_center() 
            distance =  ((xc2-xc1)**2 + (yc2-yc1)**2)**0.5
            distance /= 10
            return distance**1.5
  
    # A utility function to find the vertex with  
    # minimum distance value, from the set of vertices  
    # not yet included in shortest path tree 
    def minDistance(self, src): 
  
        # Initilaize minimum distance for next node 
        min_dist = sys.maxsize 
        min_index = src
        # Search not nearest vertex not in the  
        # shortest path tree 
        for c in range(len(self.node_list)):
            if self.sptSet[c] == False:
                node_child = self.node_list[c]
                for p in range(len(self.node_list)):
                    node_parent = self.node_list[p]
                    if self.sptSet[p] == True:
                        dist = self.get_distance(node_child, node_parent)
                        if dist < min_dist:
                            min_dist = dist
                            min_index = c
 
  
        return min_index 
  
    # Funtion that implements Dijkstra's single source  
    # shortest path algorithm for a graph represented  
    # using adjacency matrix representation 
    
    def dijkstra(self, src): 
        # Each node has a 'where from' value
        
        rx_connection_list = [0]*len(self.node_list)
        dist = [sys.maxsize]*len(self.node_list) 
        dist[src] = 0
        self.sptSet = [False]*len(self.node_list) 
        for _ in range(len(self.node_list)):
  
            # 'u' is the node, not yet chosen (not in sptSet)
            # that has the minum distance to some other node IN the sptSet
            u = self.minDistance(src) 
  
            # Now that 'u' has been chosen, put it in the sptSet
            self.sptSet[u] = True
  
            # Update dist value of the adjacent vertices  
            # of the picked vertex only if the current  
            # distance is greater than new distance and 
            # the vertex in not in the shotest path tree 
            for v in range(len(self.node_list)): 
                dist_uv = self.get_distance(self.node_list[u], self.node_list[v])
                if dist_uv != -1 and self.sptSet[v] == False:
                    if dist[v] > dist[u] + dist_uv: 
                        dist[v] = dist[u] + dist_uv
                        rx_connection_list[v] = u

                        # Track the distance from node 'v' to router
                        if self.node_list[v].type == 'router':            # Node is a router
                            self.node_list[v].connection_tier = 0           
                        elif self.node_list[u].type == 'router':          # Node is connected to router
                            self.node_list[v].connection_tier = 1           
                        else:                                             # Node is connected to another node
                            self.node_list[v].connection_tier = self.node_list[u].connection_tier + 1
                        
        return rx_connection_list