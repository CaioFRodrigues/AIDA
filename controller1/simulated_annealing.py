import controller_template as controller_template
from copy import deepcopy
from random import randint
from random import randrange
from math import exp
class Simulated_Annealing:
    '''
    Classe Simulated_Annealing - Executes Simulated_Annealing
    Call with:
        anneal = Simulated_Annealing(weights,self)
        weights = anneal.simulate(self)
    '''
    def __init__ (self, weights,controller):
        self.__weights = weights
        self.__result = controller.run_episode(weights) 
        self.__temp = 100
        
    def simulate (self, controller):
        while (self.__temp != 0):
            self.__weights = self.__get_neightbor(controller)
            self.__temp = self.__temp - 10
            print (self.__result)
        return self.__weights
 
    def __get_neightbor(self, controller)->list:
        '''
        Generate the nearest thetas for the function, for each weight passed it will try to increase and decrease,
        returning a list with twice the size
        '''
        weights = self.__weights
        N = 100
        for i in range(0,N):
            weights = self.__weights
          
     
            index = randint(0,(len(self.__weights)-1)) #Defines the index to be accessed 
            op = randint(0,1) #Decides which operation will be made
            if op == 1:
                weights[index] = weights[index] - 0.1
            else:
                weights[index] = weights[index] + 0.1
                
            result = controller.run_episode(weights)
            if (self.__choose_to_change(result,controller) == True):
                #Updates the current weights and the result
                self.__weights = weights
                self.__result = result
           
        return self.__weights
    
       
    def __choose_to_change(self,result, controller):
        '''
        Decides whether or not the current weights will changed based on the temperature
        '''

        delta = result - self.__result 
        if delta == 0:
            return False
        if (delta > 0):
            return True
        else:
            percent = exp(delta/self.__temp)
            rand =  randrange(0,100)

            if (percent < rand):
                return False
            else:
                return True
                
        