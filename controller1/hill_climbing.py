import controller_template as controller_template

class Hill_Climbing:
    
    def __init__ (self, weights):
        best_weights = []
        self.result = Controller.run_episode(weights) 
        self.new_weight_got = true  '''Flag that checks whether the last iteration has changed something or not'''
        while (best_weights != weights)
            best_weights = __generate_neighbor(weights)
            if (self.new_weight_got):
                weights = best_weights
            else:
                self.weights = weights
    
 
    def __get_best_neightbor(self, weights)->list:
        '''
        Generate the nearest thetas for the function, for each weight passed it will try to increase and decrease,
        returning a list with twice the size
        '''
        best_result = self.result
        best_weights = weights
        for theta in weights:
            '''Tries closest theta by adding 1'''
            theta = theta + 1
            current_result = Controller.run_episode(weights)
            if (current_result > best_result):
                best_result = current_result
                best_weights = weights
                
               
            '''Tries the other theta by subtracting 1 from the original theta'''
            theta = theta - 2            
            current_result = Controller.run_episode(weights)
            
            '''Returns weight to its original condition, tries again'''
            theta = theta + 1
        
        '''Checks if the result has changed'''
        if (self.result == best_result):
            self.new_weight_got = false
            
        self.result = best_result
        return best_weights
    