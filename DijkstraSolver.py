import sys 
import numpy as np

class Graph(): 
  
    def __init__(self, node_list): 
        self.node_list = node_list
        self.sptSet = []
        
    def get_distance(self, node_tx, node_rx):
        if node_tx == node_rx:
            return -1
        elif node_tx.type == 'router' and node_rx.type == 'router':
            return 1e-10
        else:
            xc1,yc1 = node_tx.get_center() 
            xc2,yc2 = node_rx.get_center() 
            p1 = node_tx.node_power
            p2 = node_rx.node_power
            if p1==0 or p2==0:
                return 1000
            distance =  ((xc2-xc1)**2 + (yc2-yc1)**2)**0.5
            distance = distance/10
            # df : forward delivery ratio (prob that data packet successfully arrives)
            # dr : backwards delivery ratio (prob that ack is successfull)
            df = np.exp(-distance/p1)
            dr = np.exp(-distance/p2)
            etx = 1/(df*dr+1e-10)
            return etx
  
    # A utility function to find the vertex with  
    # minimum distance value, from the set of vertices  
    # not yet included in shortest path tree 
    def minDistance(self, src, current_dist_list): 
  
        # Search not nearest vertex not in the  
        # shortest path tree 
        sorted_dists = np.argsort(current_dist_list)
        for node_id in sorted_dists:
            if self.sptSet[node_id] == False:
                return node_id
 
        
  
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
            u = self.minDistance(src, dist) 
  
            # Now that 'u' has been chosen, put it in the sptSet
            self.sptSet[u] = True
  
            # Update dist value of the adjacent vertices  
            # of the picked vertex only if the current  
            # distance is greater than new distance and 
            # the vertex in not in the shotest path tree 
            for v in range(len(self.node_list)): 
                if self.sptSet[v] == False:
                    dist_uv = self.get_distance(node_tx=self.node_list[u],
                                                node_rx=self.node_list[v])
                    if dist_uv != -1:
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
        
        self.rx_distance_list = dist  
        self.rx_connection_list = rx_connection_list               
        return rx_connection_list