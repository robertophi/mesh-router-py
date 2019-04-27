

import numpy as np

class RouterOptimizer():

    def __init__(self, canvas_manager):
        
        # RouterOptimizer receives a CanvasManager object as variable
        # So CanvasManager calls RouterOptimizer, and passes itself as argument
        # This way, the optimization is done in this class, using the values from the CanvasManager
        self.canvas_manager = canvas_manager

    def try_random_positions(self, node):
        best_avg_dist = 10**10
        best_coords = [400,400]
        
        for _ in range(0,25):
            [x,y] = [np.random.randint(0,800), np.random.randint(0,800)]
            node.move_to(x,y)
            self.canvas_manager.update_canvas_complete()
            average_dist = self.average_node_distance()
            if average_dist < best_avg_dist:
                best_avg_dist = average_dist
                best_coords = [x,y]
            self.canvas_manager.canvas.update()
        node.move_to(best_coords[0], best_coords[1])
        self.canvas_manager.update_canvas_complete()
        return best_coords

    def average_node_distance(self):
        ''' 
        Get the average distance from a node to a router
        '''
        distance_list = self.canvas_manager.dijkstra_graph.rx_distance_list
        return np.mean(distance_list)

    def optimize_router(self):
        router = -1
        for node in self.canvas_manager.node_list:
            if node.type == 'router':
                router = node
                continue
        if router == -1:
            return
        else:
            ## Optimize position

            self.try_random_positions(router)

            last_average_dist = self.average_node_distance()
            dx = 10
            dy = 10
            alpha = 500
            for N in range(0,100):
                min_delta = int(100/(N+3))

                # Check x-axis gradient
                router.move(10,0)
                self.canvas_manager.update_canvas_complete()
                new_average_dist = self.average_node_distance()
                delta_f = new_average_dist- last_average_dist
                delta_fx = delta_f/dx
                # Update x-axis (go back -10 units, plus mx)
                mx = - alpha*delta_fx
                mx = np.sign(mx)*max(abs(mx),min_delta)
                router.move(-10+mx,0)
                self.canvas_manager.update_canvas_complete()
                last_average_dist = self.average_node_distance()
                a = 1/0
                # Check y-axis gradient
                router.move(0,10)
                self.canvas_manager.update_canvas_complete()
                new_average_dist = self.average_node_distance()
                delta_f = new_average_dist- last_average_dist
                delta_fy = delta_f/dy
                # Update y-axis (go back 10 units, plus my)
                my = - alpha*delta_fy
                my = np.sign(my)*max(abs(my),min_delta)
                router.move(0,-10+my)                
                self.canvas_manager.update_canvas_complete()  
                last_average_dist = self.average_node_distance()

                print(last_average_dist)              

                if abs(alpha*delta_fy) < 0.1 and abs(alpha*delta_fx)<0.1 and N > 25:
                    self.canvas_manager.canvas.update()
                    return
                self.canvas_manager.canvas.update()