import controller_template as controller_template
from copy import deepcopy


class Hill_Climbing:
    '''
    Classe Hill_Climbing - Executa o Hill_Climbing alterando os thetas com -1 e com +1
    Chamar com:
        hill = Hill_Climbing(weights,self)
        weights = hill.climb(self)
    '''
    def __init__ (self, weights,controller):
        self.__weights = deepcopy(weights)
        self.__result = controller.run_episode(weights) 
        self.__new_weight_got = True    #Flag that checks whether the last iteration has changed something or not

    def climb (self, controller):
        while (self.__new_weight_got == True):
            self.__weights = self.__get_best_neightbor(controller)
        
        return self.__weights
 
    def __get_best_neightbor(self, controller)->list:
        '''
        Generate the nearest thetas for the function, for each weight passed it will try to increase and decrease,
        returning a list with twice the size
        '''
        best_result = self.__result
        best_weights = self.__weights
        for index,theta in enumerate(self.__weights):
       
            #Tries closest theta by adding 1
            self.__weights[index] = self.__weights[index] + 1
            current_result = controller.run_episode(self.__weights)
            
            #Checks if current weight is the best one
            if (current_result > best_result):
                best_result = current_result
                best_weights = self.__weights
                
               
               
            #Tries the other theta by subtracting 1 from the original theta
            self.__weights[index] = self.__weights[index] - 2            
            current_result = controller.run_episode(self.__weights)
            
            #Checks if current weight is the best one
            if current_result > best_result:
                best_result = current_result
                best_weights = self.__weights
                
            #Returns weight to its original condition, tries again
            self.__weights[index] = self.__weights[index] + 1
            
            
        #Checks if the result has changed
        if (self.__result == best_result):
            self.__new_weight_got = False
            
        self.__result = best_result
        return best_weights
    