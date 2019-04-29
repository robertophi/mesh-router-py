
from scipy.optimize import minimize
import numpy as np


class RouterOptimizer():

    def __init__(self, canvas_manager):

        # RouterOptimizer receives a CanvasManager object as variable
        # So CanvasManager calls RouterOptimizer, and passes itself as argument
        # This way, the optimization is done in this class, using the values from the CanvasManager
        self.canvas_manager = canvas_manager

    def try_random_positions(self, node):
        best_avg_dist = 10**10
        best_coords = [400, 400]

        for j in range(0, 10):
            for i in range(0, 10):
                x = 80 * i + 40
                y = 80 * j + 40

                node.move_to(x, y)
                self.canvas_manager.update_canvas_complete()
                self.canvas_manager.canvas.update()

                average_dist = self.average_node_distance()
                if average_dist < best_avg_dist:
                    best_avg_dist = average_dist
                    best_coords = [x, y]
        node.move_to(best_coords[0], best_coords[1])
        self.canvas_manager.update_canvas_complete()
        self.canvas_manager.canvas.update()
        return best_coords

    def get_average_node_distance(self):
        ''' 
        Get the average distance from a node to a router
        '''
        node_dist_list = []
        distance_list = self.canvas_manager.dijkstra_graph.rx_distance_list
        for i, node in enumerate(self.canvas_manager.node_list):
            if node.type != 'router':
                node_dist_list.append(distance_list[i])

        self.avg_distance = np.mean(node_dist_list)
        return self.avg_distance

    # Do this so we can overwrite this method on the WindowsManager
    def average_node_distance(self):
        return self.get_average_node_distance()



    def optimize_router(self):
        router = -1
        for node in self.canvas_manager.node_list:
            if node.type == 'router':
                router = node
                continue
        if router == -1:
            return
        else:
            # Optimize position

            self.try_random_positions(router)

            last_average_dist = self.average_node_distance()
            dx = 10
            dy = 10
            alpha = 500
            delta_movement = 1
            for N in range(0, 100):
                min_delta = int(100 / (N + 3))

                # Check x-axis gradient
                router.move(delta_movement, 0)
                self.canvas_manager.update_canvas_complete()
                new_average_dist = self.average_node_distance()
                delta_f = new_average_dist - last_average_dist
                delta_fx = delta_f / dx
                # Update x-axis (go back -10 units, plus mx)
                mx = - alpha * delta_fx
                mx = np.sign(mx) * max(abs(mx), min_delta)
                router.move(-delta_movement + mx, 0)
                self.canvas_manager.update_canvas_complete()
                last_average_dist = self.average_node_distance()

                # Check y-axis gradient
                router.move(0, delta_movement)
                self.canvas_manager.update_canvas_complete()
                new_average_dist = self.average_node_distance()
                delta_f = new_average_dist - last_average_dist
                delta_fy = delta_f / dy
                # Update y-axis (go back 10 units, plus my)
                my = - alpha * delta_fy
                my = np.sign(my) * max(abs(my), min_delta)
                router.move(0, -delta_movement + my)
                self.canvas_manager.update_canvas_complete()
                last_average_dist = self.average_node_distance()

                print(last_average_dist)

                if abs(alpha * delta_fy) < 0.1 and abs(alpha * delta_fx) < 0.1 and N > 25:
                    self.canvas_manager.canvas.update()
                    return
                self.canvas_manager.canvas.update()

    def optimizer_function(self, X):

        router = -1
        for node in self.canvas_manager.node_list:
            if node.type == 'router':
                router = node
                continue

        x = X[0]
        y = X[1]
        router.move_to(x, y)
        self.canvas_manager.update_canvas_complete()
        self.canvas_manager.canvas.update()
        avg = self.average_node_distance()
        print(avg)
        return avg

    def optimize_router_scipy(self):
        router = -1
        for node in self.canvas_manager.node_list:
            if node.type == 'router':
                router = node
                continue
        if router == -1:
            return
        else:
            # Optimize position

            self.try_random_positions(router)

            X0 = [router.center]
            res = minimize(self.optimizer_function, X0, options={'eps': 0.001})
            print(res)
